"use strict";

/*
========================================
Romantic Love Site
JavaScript
========================================
*/


// ======================================
// گرفتن عناصر صفحه
// ======================================

const loveButton = document.getElementById("loveButton");
const secret = document.getElementById("secret");

const musicButton = document.getElementById("musicButton");
const music = document.getElementById("music");


// ======================================
// تنظیمات
// ======================================

const HEART_COUNT = 30;
const HEART_LIFETIME = 3000;


// ======================================
// نمایش پیام مخفی
// ======================================

if (loveButton && secret) {

    loveButton.addEventListener("click", () => {

        secret.classList.add("show");

        loveButton.textContent =
            "❤️ حالا دیگه می‌دونی";

        createHearts(HEART_COUNT);

    });

}


// ======================================
// سیستم موزیک
// ======================================

let musicPlaying = false;

if (musicButton && music) {

    musicButton.addEventListener("click", async () => {

        try {

            if (!musicPlaying) {

                await music.play();

                musicPlaying = true;

                musicButton.textContent = "🔊";

            } else {

                music.pause();

                musicPlaying = false;

                musicButton.textContent = "🎵";

            }

        } catch (error) {

            console.log(
                "Music could not be played:",
                error
            );

        }

    });

}


// ======================================
// ساخت قلب‌های شناور
// ======================================

function createHearts(count = 20) {

    for (let i = 0; i < count; i++) {

        setTimeout(() => {

            createSingleHeart();

        }, i * 80);

    }

}


// ======================================
// ساخت یک قلب
// ======================================

function createSingleHeart() {

    const heart =
        document.createElement("div");


    heart.className =
        "floating-heart";


    heart.textContent = "♥";


    // موقعیت افقی تصادفی

    heart.style.left =
        `${Math.random() * 100}%`;


    // شروع از پایین

    heart.style.bottom =
        "15%";


    // اندازه تصادفی

    const size =
        15 + Math.random() * 30;


    heart.style.fontSize =
        `${size}px`;


    // کمی شفافیت تصادفی

    heart.style.opacity =
        0.7 + Math.random() * 0.3;


    document.body.appendChild(
        heart
    );


    // حذف بعد از انیمیشن

    setTimeout(() => {

        heart.remove();

    }, HEART_LIFETIME);

}


// ======================================
// قلب با کلیک روی صفحه
// ======================================

document.addEventListener(
    "click",
    (event) => {

        // اگر روی دکمه موزیک یا دکمه اصلی کلیک شد
        // تعداد قلب جداگانه تولید می‌شود

        if (
            event.target === musicButton ||
            event.target === loveButton
        ) {
            return;
        }


        createClickHeart(
            event.clientX,
            event.clientY
        );

    }
);


// ======================================
// قلبی که از محل کلیک ظاهر می‌شود
// ======================================

function createClickHeart(x, y) {

    const heart =
        document.createElement("div");


    heart.className =
        "floating-heart";


    heart.textContent =
        Math.random() > 0.5
            ? "♥"
            : "❤";


    heart.style.position =
        "fixed";


    heart.style.left =
        `${x}px`;


    heart.style.top =
        `${y}px`;


    heart.style.bottom =
        "auto";


    heart.style.fontSize =
        `${15 + Math.random() * 25}px`;


    heart.style.pointerEvents =
        "none";


    document.body.appendChild(
        heart
    );


    setTimeout(() => {

        heart.remove();

    }, HEART_LIFETIME);

}


// ======================================
// افکت اولیه صفحه
// ======================================

window.addEventListener(
    "load",
    () => {

        setTimeout(() => {

            createHearts(10);

        }, 700);

    }
);


// ======================================
// جلوگیری از خطای تصویر خالی
// ======================================

const photo =
    document.querySelector(
        ".photo-container img"
    );


if (photo) {

    photo.addEventListener(
        "error",
        () => {

            photo.style.display =
                "none";

        }
    );

}


// ======================================
// کنترل صفحه با کیبورد
// ======================================

document.addEventListener(
    "keydown",
    (event) => {

        // Space = نمایش پیام

        if (
            event.code === "Space" &&
            loveButton
        ) {

            event.preventDefault();

            loveButton.click();

        }


        // M = موزیک

        if (
            event.key.toLowerCase() === "m" &&
            musicButton
        ) {

            musicButton.click();

        }

    }
);


// ======================================
// وقتی صفحه بسته می‌شود
// ======================================

window.addEventListener(
    "beforeunload",
    () => {

        if (music) {

            music.pause();

        }

    }
);
