from pathlib import Path
import shutil
import zipfile
import re


BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "template"
OUTPUT_DIR = BASE_DIR / "output"


def safe_name(name):
    name = name.strip()

    name = re.sub(
        r'[<>:"/\\|?*]',
        '',
        name
    )

    return name or "love-site"


def create_site(
    name,
    message,
    color="#087fc9",
    music="",
    photo=""
):

    name = safe_name(name)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not TEMPLATE_DIR.exists():
        raise FileNotFoundError(
            "پوشه template پیدا نشد."
        )

    site_dir = OUTPUT_DIR / name

    if site_dir.exists():
        shutil.rmtree(site_dir)

    shutil.copytree(
        TEMPLATE_DIR,
        site_dir
    )


    # --------------------------
    # جایگزینی متن‌ها
    # --------------------------

    replacements = {

        "{{NAME}}": name,

        "{{MESSAGE}}": message,

        "{{MUSIC}}": music,

        "{{PHOTO}}": photo

    }


    text_extensions = {
        ".html",
        ".css",
        ".js",
        ".json",
        ".txt",
        ".svg"
    }


    for file in site_dir.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() not in text_extensions:
            continue

        try:

            content = file.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            continue


        # متن‌ها

        for old, new in replacements.items():

            content = content.replace(
                old,
                str(new)
            )


        # --------------------------
        # تغییر رنگ اصلی CSS
        # --------------------------

        if file.name == "style.css":

            content = re.sub(

                r'--main-color\s*:\s*#[0-9a-fA-F]{6}\s*;',

                f'--main-color: {color};',

                content

            )


        file.write_text(
            content,
            encoding="utf-8"
        )


    # --------------------------
    # ساخت ZIP
    # --------------------------

    zip_path = (
        OUTPUT_DIR /
        f"{name}-love-site.zip"
    )


    if zip_path.exists():
        zip_path.unlink()


    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        for file in site_dir.rglob("*"):

            if file.is_file():

                archive.write(
                    file,
                    file.relative_to(site_dir)
                )


    return zip_path


# --------------------------
# تست
# --------------------------

if __name__ == "__main__":

    result = create_site(

        name="نرگس",

        message=(
            "تو قشنگ‌ترین اتفاقی هستی "
            "که دوست دارم بیشتر بشناسمت. 💙"
        ),

        color="#087fc9",

        music="",

        photo=""
    )


    print()
    print("✅ سایت ساخته شد!")
    print()
    print("📦 فایل:")
    print(result)