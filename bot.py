import os
import shutil
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

from generator import create_site


# ==========================================
# تنظیمات
# ==========================================

TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = Path(__file__).resolve().parent

TEMP_DIR = BASE_DIR / "temp"

TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# مراحل گفتگو
# ==========================================

NAME = 1
COLOR = 2
MESSAGE = 3
PHOTO = 4
MUSIC = 5


# ==========================================
# اطلاعات موقت کاربران
# ==========================================

users = {}


# ==========================================
# /start
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    users[user_id] = {
        "name": "",
        "color": "#087fc9",
        "message": "",
        "photo": "",
        "music": "",
    }

    await update.message.reply_text(
        "💙 به Love Site Bot خوش اومدی!\n\n"
        "قراره برات یک سایت عاشقانه اختصاصی بسازم.\n\n"
        "اول اسم شخص موردنظر رو بفرست ❤️"
    )

    return NAME


# ==========================================
# دریافت اسم
# ==========================================

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    name = update.message.text.strip()

    if not name:

        await update.message.reply_text(
            "❌ لطفاً یک اسم بفرست."
        )

        return NAME


    users[user_id]["name"] = name


    await update.message.reply_text(
        "🎨 حالا رنگ اصلی سایت رو انتخاب کن.\n\n"

        "💙 آبی\n"
        "💗 صورتی\n"
        "💜 بنفش\n"
        "❤️ قرمز\n"
        "💚 سبز\n\n"

        "مثلاً بنویس: آبی"
    )

    return COLOR


# ==========================================
# تبدیل اسم رنگ به کد
# ==========================================

def convert_color(color):

    colors = {

        "آبی": "#087fc9",
        "ابی": "#087fc9",
        "blue": "#087fc9",

        "صورتی": "#e83e8c",
        "صورتی": "#e83e8c",
        "pink": "#e83e8c",

        "بنفش": "#8b5cf6",
        "purple": "#8b5cf6",

        "قرمز": "#ef4444",
        "red": "#ef4444",

        "سبز": "#10b981",
        "green": "#10b981",

    }

    return colors.get(
        color.strip().lower(),
        "#087fc9"
    )


# ==========================================
# دریافت رنگ
# ==========================================

async def get_color(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    color = convert_color(
        update.message.text
    )

    users[user_id]["color"] = color


    await update.message.reply_text(
        "💌 حالا متن عاشقانه‌ای که می‌خوای "
        "داخل سایت نمایش داده بشه رو بفرست.\n\n"

        "می‌تونی چند خط بنویسی."
    )

    return MESSAGE


# ==========================================
# دریافت متن
# ==========================================

async def get_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    users[user_id]["message"] = (
        update.message.text
    )


    await update.message.reply_text(
        "📸 حالا اگر می‌خوای عکس داخل سایت "
        "قرار بگیره، عکس رو همینجا بفرست.\n\n"

        "اگر عکس نمی‌خوای، بنویس:\n"
        "ندارم"
    )

    return PHOTO


# ==========================================
# دریافت عکس
# ==========================================

async def get_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    # اگر کاربر عکس نفرستاده
    if not update.message.photo:

        text = update.message.text

        if text and text.strip() == "ندارم":

            users[user_id]["photo"] = ""

            await update.message.reply_text(
                "🎵 حالا اگر موزیک می‌خوای، "
                "فایل MP3 رو بفرست.\n\n"

                "اگر موزیک نمی‌خوای، بنویس:\n"
                "ندارم"
            )

            return MUSIC


        await update.message.reply_text(
            "📸 لطفاً عکس رو بفرست یا بنویس «ندارم»."
        )

        return PHOTO


    # دریافت بهترین کیفیت عکس
    photo = update.message.photo[-1]


    file = await context.bot.get_file(
        photo.file_id
    )


    user_folder = TEMP_DIR / str(user_id)

    user_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    photo_path = (
        user_folder / "photo.jpg"
    )


    await file.download_to_drive(
        photo_path
    )


    # برای سایت
    users[user_id]["photo"] = (
        "photo.jpg"
    )


    await update.message.reply_text(
        "✅ عکس دریافت شد.\n\n"

        "🎵 حالا اگر موزیک می‌خوای، "
        "فایل MP3 رو بفرست.\n\n"

        "اگر موزیک نمی‌خوای، بنویس:\n"
        "ندارم"
    )

    return MUSIC


# ==========================================
# دریافت موزیک
# ==========================================

async def get_music(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user_folder = TEMP_DIR / str(user_id)


    # بدون موزیک
    if not update.message.audio:

        text = update.message.text

        if text and text.strip() == "ندارم":

            users[user_id]["music"] = ""

        else:

            await update.message.reply_text(
                "🎵 لطفاً فایل MP3 رو بفرست "
                "یا بنویس «ندارم»."
            )

            return MUSIC

    else:

        audio = update.message.audio


        file = await context.bot.get_file(
            audio.file_id
        )


        user_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        music_path = (
            user_folder / "music.mp3"
        )


        await file.download_to_drive(
            music_path
        )


        users[user_id]["music"] = (
            "music.mp3"
        )


    # ساخت سایت
    await update.message.reply_text(
        "⏳ دارم سایت رو می‌سازم...\n\n"
        "🌌 طراحی صفحه\n"
        "❤️ ساخت افکت‌ها\n"
        "✨ شخصی‌سازی\n"
        "📦 ساخت فایل ZIP"
    )


    user = users[user_id]


    try:

        zip_path = create_site(

            name=user["name"],

            message=user["message"],

            color=user["color"],

            music=user["music"],

            photo=user["photo"]

        )


        # ==================================
        # اضافه کردن عکس و موزیک به ZIP
        # ==================================

        # generator فایل ZIP را ساخته.
        # حالا فایل‌های رسانه‌ای را داخل
        # همان ZIP قرار می‌دهیم.

        import zipfile


        with zipfile.ZipFile(
            zip_path,
            "a",
            zipfile.ZIP_DEFLATED
        ) as archive:


            if user["photo"]:

                photo_file = (
                    user_folder /
                    "photo.jpg"
                )

                if photo_file.exists():

                    archive.write(
                        photo_file,
                        "photo.jpg"
                    )


            if user["music"]:

                music_file = (
                    user_folder /
                    "music.mp3"
                )

                if music_file.exists():

                    archive.write(
                        music_file,
                        "music.mp3"
                    )


        # ارسال ZIP

        await update.message.reply_document(

            document=open(
                zip_path,
                "rb"
            ),

            caption=(
                "🎉 سایت آماده شد!\n\n"

                f"💙 نام: {user['name']}\n"

                "📦 فایل ZIP آماده آپلود روی Netlify است.\n\n"

                "🚀 فایل رو دانلود کن و داخل "
                "Netlify Drop بنداز."
            )

        )


    except Exception as error:

        print(
            "ERROR:",
            error
        )

        await update.message.reply_text(
            "❌ هنگام ساخت سایت خطایی اتفاق افتاد.\n\n"
            f"جزئیات: {error}"
        )


    finally:

        # پاک کردن اطلاعات موقت
        if user_folder.exists():

            shutil.rmtree(
                user_folder,
                ignore_errors=True
            )


        users.pop(
            user_id,
            None
        )


    return ConversationHandler.END


# ==========================================
# لغو
# ==========================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    users.pop(
        user_id,
        None
    )


    await update.message.reply_text(
        "❌ ساخت سایت لغو شد.\n\n"
        "هر وقت خواستی دوباره /start رو بزن."
    )


    return ConversationHandler.END


# ==========================================
# اجرای ربات
# ==========================================

def main():

    if TOKEN == "TOKEN_BOT":

        print(
            "❌ ابتدا TOKEN_BOT را با توکن رباتت جایگزین کن."
        )

        return


    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    conversation = ConversationHandler(

        entry_points=[
            CommandHandler(
                "start",
                start
            )
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.TEXT &
                    ~filters.COMMAND,
                    get_name
                )
            ],

            COLOR: [
                MessageHandler(
                    filters.TEXT &
                    ~filters.COMMAND,
                    get_color
                )
            ],

            MESSAGE: [
                MessageHandler(
                    filters.TEXT &
                    ~filters.COMMAND,
                    get_message
                )
            ],

            PHOTO: [
                MessageHandler(
                    filters.PHOTO |
                    (
                        filters.TEXT &
                        ~filters.COMMAND
                    ),
                    get_photo
                )
            ],

            MUSIC: [
                MessageHandler(
                    filters.AUDIO |
                    (
                        filters.TEXT &
                        ~filters.COMMAND
                    ),
                    get_music
                )
            ],

        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel
            )
        ],

        allow_reentry=True
    )


    application.add_handler(
        conversation
    )


    print(
        "🤖 LoveBot is running..."
    )


    application.run_polling()


# ==========================================
# شروع
# ==========================================

if __name__ == "__main__":
    main()