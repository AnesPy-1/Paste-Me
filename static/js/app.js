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
});
