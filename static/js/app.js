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

    const uploadForm = document.getElementById("upload-form");
    const uploadButton = document.getElementById("upload-button");
    const uploadBar = document.getElementById("upload-bar");
    const uploadPercent = document.getElementById("upload-percent");
    const uploadStatus = document.getElementById("upload-status");
    const uploadProgress = document.getElementById("upload-progress");

    if (uploadForm && uploadButton && uploadBar && uploadPercent && uploadStatus && uploadProgress) {
        uploadForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const formData = new FormData(uploadForm);
            const xhr = new XMLHttpRequest();
            xhr.open("POST", uploadForm.action, true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            const csrfToken = uploadForm.querySelector("input[name='csrfmiddlewaretoken']")?.value;
            if (csrfToken) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }

            const resetState = () => {
                uploadButton.disabled = false;
                uploadButton.textContent = "آپلود فایل";
                uploadProgress.hidden = true;
            };

            xhr.upload.addEventListener("loadstart", () => {
                uploadButton.disabled = true;
                uploadButton.textContent = "در حال آپلود...";
                uploadProgress.hidden = false;
                uploadBar.style.width = "0%";
                uploadPercent.textContent = "۰٪";
                uploadStatus.textContent = "";
            });

            xhr.upload.addEventListener("progress", (e) => {
                if (!e.lengthComputable) return;
                const percent = Math.round((e.loaded / e.total) * 100);
                uploadBar.style.width = `${percent}%`;
                uploadPercent.textContent = `${percent.toLocaleString("fa-IR")}%`;
            });

            xhr.addEventListener("readystatechange", () => {
                if (xhr.readyState !== XMLHttpRequest.DONE) return;
                resetState();

                if (xhr.status >= 200 && xhr.status < 300) {
                    uploadBar.style.width = "100%";
                    uploadPercent.textContent = "۱۰۰٪";
                    uploadStatus.textContent = "آپلود موفق بود؛ در حال انتقال...";
                    try {
                        const data = JSON.parse(xhr.responseText);
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        }
                    } catch (err) {
                        uploadStatus.textContent = "پاسخ نامعتبر از سرور";
                    }
                } else {
                    let message = "آپلود ناموفق بود. لطفاً دوباره تلاش کنید.";
                    try {
                        const data = JSON.parse(xhr.responseText);
                        if (data.errors?.file) {
                            message = data.errors.file.join(" ");
                        }
                    } catch (err) {}
                    uploadStatus.textContent = message;
                    uploadProgress.classList.add("shake");
                    setTimeout(() => uploadProgress.classList.remove("shake"), 400);
                }
            });

            xhr.addEventListener("error", () => {
                resetState();
                uploadStatus.textContent = "خطا در ارتباط با سرور";
            });

            xhr.send(formData);
        });
    }
});
