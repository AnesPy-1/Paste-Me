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
        const storedTheme = localStorage.getItem("theme");
        const initialTheme = storedTheme || "dark";
        document.body.dataset.theme = initialTheme;
        themeToggle.textContent = initialTheme === "dark" ? "حالت روشن" : "حالت تاریک";

        themeToggle.addEventListener("click", () => {
            const nextTheme = document.body.dataset.theme === "dark" ? "light" : "dark";
            document.body.dataset.theme = nextTheme;
            localStorage.setItem("theme", nextTheme);
            themeToggle.textContent = nextTheme === "dark" ? "حالت روشن" : "حالت تاریک";
        });
    }
});
