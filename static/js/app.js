document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab-button");
    const panels = document.querySelectorAll(".panel");

    tabs.forEach((button) => {
        button.addEventListener("click", () => {
            tabs.forEach((item) => item.classList.remove("active"));
            panels.forEach((panel) => panel.classList.remove("active"));
            button.classList.add("active");
            document.getElementById(button.dataset.target)?.classList.add("active");
        });
    });

    document.querySelectorAll(".copy-button").forEach((button) => {
        button.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(button.dataset.copyText || "");
                button.textContent = "کپی شد";
            } catch {
                button.textContent = "کپی ناموفق بود";
            }
        });
    });

    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
        const icon = themeToggle.querySelector(".theme-toggle__icon");
        const label = themeToggle.querySelector(".theme-toggle__label");

        const storedTheme = localStorage.getItem("theme");
        const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
        const initialTheme = storedTheme || (prefersDark ? "dark" : "light");

        const applyTheme = (theme) => {
            document.body.dataset.theme = theme;
            localStorage.setItem("theme", theme);
            const isDark = theme === "dark";
            icon.textContent = isDark ? "🌙" : "☀️";
            label.textContent = isDark ? "حالت روشن" : "حالت تاریک";
            themeToggle.setAttribute("aria-pressed", String(isDark));
        };

        applyTheme(initialTheme);

        themeToggle.addEventListener("click", () => {
            const nextTheme = document.body.dataset.theme === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
        });
    }
});
