/* static/js/app.js */
"use strict";

/**
 * Initialize shared frontend behaviors used across templates.
 */
document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initLanguageSelector();
    initNavbarAutoClose();
});

/**
 * Applies persisted theme and wires the toggle when present.
 */
function initThemeToggle() {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const savedTheme = localStorage.getItem("theme");
    const isDark = savedTheme === "dark";

    document.body.classList.toggle("dark-mode", isDark);

    if (themeToggle) {
        themeToggle.checked = isDark;
        themeToggle.addEventListener("change", function onThemeChange() {
            const dark = this.checked;
            document.body.classList.toggle("dark-mode", dark);
            localStorage.setItem("theme", dark ? "dark" : "light");
            if (themeIcon) {
                themeIcon.textContent = dark ? "🌙" : "☀️";
            }
        });
    }

    if (themeIcon) {
        themeIcon.textContent = isDark ? "🌙" : "☀️";
    }
}

/**
 * Submits language form when selector changes.
 */
function initLanguageSelector() {
    const languageSelect = document.getElementById("language-select");
    const languageForm = document.getElementById("language-form");

    if (!languageSelect || !languageForm) {
        return;
    }

    languageSelect.addEventListener("change", () => {
        languageForm.submit();
    });
}

/**
 * Closes expanded mobile navbar when clicking outside.
 */
function initNavbarAutoClose() {
    document.addEventListener("click", (event) => {
        const navbarCollapse = document.getElementById("navbarNav");
        const toggler = document.querySelector(".navbar-toggler");

        if (!navbarCollapse || !toggler || !navbarCollapse.classList.contains("show")) {
            return;
        }

        if (!navbarCollapse.contains(event.target) && !toggler.contains(event.target)) {
            if (typeof bootstrap !== "undefined" && bootstrap.Collapse) {
                new bootstrap.Collapse(navbarCollapse, { toggle: true });
            }
        }
    });
}


