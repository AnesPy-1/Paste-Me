(() => {
    const doc = document;
    const body = doc.body;

    const rafThrottle = (fn) => {
        let ticking = false;
        return (...args) => {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(() => {
                fn(...args);
                ticking = false;
            });
        };
    };

    const detectLiteMode = () => {
        const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
        const isCoarsePointer = window.matchMedia?.("(hover: none), (pointer: coarse)")?.matches;
        const lowCpu = typeof navigator.hardwareConcurrency === "number" && navigator.hardwareConcurrency <= 4;
        const lowMemory = typeof navigator.deviceMemory === "number" && navigator.deviceMemory <= 4;

        if (prefersReducedMotion || lowCpu || lowMemory || isCoarsePointer) {
            body.classList.add("is-lite");
        }
    };

    const initPreloader = () => {
        const preloader = doc.getElementById("preloader");
        if (!preloader) return;

        const hide = () => {
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    preloader.classList.add("preloader--hidden");
                    preloader.addEventListener(
                        "transitionend",
                        () => {
                            preloader.remove();
                        },
                        { once: true }
                    );
                });
            });
        };

        if (doc.readyState === "complete") {
            hide();
            return;
        }

        window.addEventListener("load", hide, { once: true });
        setTimeout(hide, 2500);
    };

    const initTabs = () => {
        const tabs = doc.querySelectorAll(".tab-button[data-target]");
        const panels = doc.querySelectorAll(".panel");
        if (!tabs.length || !panels.length) return;

        tabs.forEach((button) => {
            button.addEventListener("click", () => {
                const targetId = button.dataset.target;
                if (!targetId) return;

                tabs.forEach((item) => item.classList.remove("active"));
                panels.forEach((panel) => panel.classList.remove("active"));

                button.classList.add("active");
                doc.getElementById(targetId)?.classList.add("active");
            });
        });
    };

    const initCopyButtons = () => {
        doc.querySelectorAll(".copy-button").forEach((button) => {
            button.addEventListener("click", async () => {
                const original = button.textContent;
                try {
                    await navigator.clipboard.writeText(button.dataset.copyText || "");
                    button.textContent = "\u06A9\u067E\u06CC \u0634\u062F";
                } catch {
                    button.textContent = "\u06A9\u067E\u06CC \u0646\u0627\u0645\u0648\u0641\u0642 \u0628\u0648\u062F";
                }

                setTimeout(() => {
                    button.textContent = original;
                }, 1400);
            });
        });
    };

    const initThemeToggle = () => {
        const themeToggle = doc.getElementById("theme-toggle");
        if (!themeToggle) return;

        const icon = themeToggle.querySelector(".theme-toggle__icon");
        const label = themeToggle.querySelector(".theme-toggle__label");

        const storedTheme = localStorage.getItem("theme");
        const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)")?.matches;
        const initialTheme = storedTheme || (prefersDark ? "dark" : "light");

        const applyTheme = (theme) => {
            body.dataset.theme = theme;
            localStorage.setItem("theme", theme);

            const isDark = theme === "dark";
            if (icon) icon.textContent = isDark ? "\u263D" : "\u2600";
            if (label) label.textContent = isDark ? "\u062D\u0627\u0644\u062A \u0631\u0648\u0634\u0646" : "\u062D\u0627\u0644\u062A \u062A\u0627\u0631\u06CC\u06A9";
            themeToggle.setAttribute("aria-pressed", String(isDark));
        };

        applyTheme(initialTheme);

        themeToggle.addEventListener("click", () => {
            const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
        });
    };

    const initTopbarScroll = () => {
        const topbar = doc.querySelector(".topbar");
        if (!topbar) return;

        const onScroll = rafThrottle(() => {
            topbar.classList.toggle("topbar--scrolled", window.scrollY > 8);
        });

        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    };

    const initPressFeedback = () => {
        const interactiveSelector = ".primary-button, .tab-button, .download-link, .theme-toggle";
        doc.querySelectorAll(interactiveSelector).forEach((element) => {
            const release = () => element.classList.remove("is-pressed");
            element.addEventListener("pointerdown", () => element.classList.add("is-pressed"), { passive: true });
            element.addEventListener("pointerup", release, { passive: true });
            element.addEventListener("pointercancel", release, { passive: true });
            element.addEventListener("pointerleave", release, { passive: true });
        });
    };

    const initRevealObserver = () => {
        if (!("IntersectionObserver" in window) || body.classList.contains("is-lite")) {
            doc.querySelectorAll(".card, .status-badge, .actions").forEach((el) => {
                el.classList.add("is-visible");
            });
            return;
        }

        const targets = doc.querySelectorAll(".card, .status-badge, .actions");
        if (!targets.length) return;

        const observer = new IntersectionObserver(
            (entries, obs) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add("is-visible");
                    obs.unobserve(entry.target);
                });
            },
            {
                threshold: 0.15,
                rootMargin: "0px 0px -8% 0px"
            }
        );

        targets.forEach((el) => {
            el.classList.add("reveal");
            observer.observe(el);
        });
    };

    const initFlashMessages = () => {
        const dismiss = (flash) => {
            flash.classList.add("flash--leave");
            flash.addEventListener(
                "animationend",
                () => {
                    flash.remove();
                },
                { once: true }
            );
        };

        const bindFlash = (flash, timeoutMs = 6200) => {
            const closeButton = flash.querySelector("[data-flash-dismiss]");
            if (closeButton) {
                closeButton.addEventListener("click", () => dismiss(flash), { passive: true });
            }
            setTimeout(() => dismiss(flash), timeoutMs);
        };

        const ensureFlashStack = () => {
            let stack = doc.querySelector(".flash-stack");
            if (stack) return stack;

            stack = doc.createElement("section");
            stack.className = "flash-stack";
            stack.setAttribute("aria-live", "polite");
            stack.setAttribute("aria-label", "پیام‌های سیستم");

            const topbar = doc.querySelector(".topbar");
            if (topbar?.parentNode) {
                topbar.parentNode.insertBefore(stack, topbar.nextSibling);
            } else {
                body.prepend(stack);
            }
            return stack;
        };

        const pushFlash = (message, type = "error") => {
            const stack = ensureFlashStack();
            const flash = doc.createElement("article");
            flash.className = `flash flash--${type}`;
            flash.setAttribute("role", "status");

            const text = doc.createElement("p");
            text.className = "flash__text";
            text.textContent = message;

            const close = doc.createElement("button");
            close.type = "button";
            close.className = "flash__close";
            close.setAttribute("data-flash-dismiss", "");
            close.setAttribute("aria-label", "بستن پیام");
            close.textContent = "×";

            flash.append(text, close);
            stack.appendChild(flash);
            bindFlash(flash);
        };

        const flashes = doc.querySelectorAll(".flash");
        flashes.forEach((flash) => {
            bindFlash(flash);
        });

        return { pushFlash };
    };

    const initUploadForm = (pushFlash) => {
        const uploadForm = doc.getElementById("upload-form");
        const uploadButton = doc.getElementById("upload-button");
        const uploadBar = doc.getElementById("upload-bar");
        const uploadPercent = doc.getElementById("upload-percent");
        const uploadStatus = doc.getElementById("upload-status");
        const uploadProgress = doc.getElementById("upload-progress");
        const fileInput = uploadForm?.querySelector("input[type='file']");

        if (!uploadForm || !uploadButton || !uploadBar || !uploadPercent || !uploadStatus || !uploadProgress || !fileInput) {
            return;
        }

        const maxUploadBytes = Number(uploadForm.dataset.maxUploadBytes || fileInput.dataset.maxSize || 200 * 1024 * 1024);
        let rafId = null;
        let nextProgress = 0;

        const formatBytes = (bytes) => {
            const mb = bytes / (1024 * 1024);
            return `${mb.toLocaleString("fa-IR", { maximumFractionDigits: mb >= 100 ? 0 : 1 })} \u0645\u06AF\u0627\u0628\u0627\u06CC\u062A`;
        };

        const getOversizeMessage = () => {
            if (maxUploadBytes === 200 * 1024 * 1024) {
                return "\u062D\u062C\u0645 \u0641\u0627\u06CC\u0644 \u0627\u0632 \u062D\u062F \u0645\u062C\u0627\u0632 \u0628\u06CC\u0634\u062A\u0631 \u0627\u0633\u062A. \u062D\u062F\u0627\u06A9\u062B\u0631 \u06F2\u06F0\u06F0 \u0645\u06AF\u0627\u0628\u0627\u06CC\u062A \u0645\u062C\u0627\u0632 \u0627\u0633\u062A.";
            }
            return `\u062D\u062C\u0645 \u0641\u0627\u06CC\u0644 \u0627\u0632 \u062D\u062F \u0645\u062C\u0627\u0632 \u0628\u06CC\u0634\u062A\u0631 \u0627\u0633\u062A. \u062D\u062F\u0627\u06A9\u062B\u0631 ${formatBytes(maxUploadBytes)} \u0645\u062C\u0627\u0632 \u0627\u0633\u062A.`;
        };

        const setProgress = (value) => {
            nextProgress = Math.max(0, Math.min(1, value));
            if (rafId !== null) return;

            rafId = requestAnimationFrame(() => {
                uploadBar.style.setProperty("--progress", nextProgress.toFixed(3));
                uploadPercent.textContent = `${Math.round(nextProgress * 100).toLocaleString("fa-IR")}%`;
                rafId = null;
            });
        };

        const resetState = () => {
            uploadButton.disabled = false;
            uploadButton.textContent = "\u0622\u067E\u0644\u0648\u062F \u0641\u0627\u06CC\u0644";
            uploadProgress.hidden = true;
        };

        const showValidationError = (message) => {
            uploadProgress.hidden = true;
            if (typeof pushFlash === "function") {
                pushFlash(message, "error");
                return;
            }
            uploadStatus.textContent = message;
        };

        const getSelectedFile = () => fileInput.files?.[0] || null;

        const validateSelectedFile = () => {
            const selectedFile = getSelectedFile();
            if (!selectedFile) return true;
            if (selectedFile.size <= maxUploadBytes) return true;

            const message = getOversizeMessage();
            showValidationError(message);
            fileInput.value = "";
            return false;
        };

        fileInput.addEventListener("change", () => {
            validateSelectedFile();
        });

        uploadForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const selectedFile = getSelectedFile();
            if (!selectedFile) {
                showValidationError("\u0644\u0637\u0641\u0627\u064B \u0627\u0628\u062A\u062F\u0627 \u06CC\u06A9 \u0641\u0627\u06CC\u0644 \u0627\u0646\u062A\u062E\u0627\u0628 \u06A9\u0646\u06CC\u062F.");
                return;
            }
            if (!validateSelectedFile()) {
                return;
            }

            const formData = new FormData(uploadForm);
            const xhr = new XMLHttpRequest();
            xhr.open("POST", uploadForm.action, true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            const csrfToken = uploadForm.querySelector("input[name='csrfmiddlewaretoken']")?.value;
            if (csrfToken) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }

            xhr.upload.addEventListener("loadstart", () => {
                uploadButton.disabled = true;
                uploadButton.textContent = "\u062F\u0631 \u062D\u0627\u0644 \u0622\u067E\u0644\u0648\u062F...";
                uploadProgress.hidden = false;
                setProgress(0);
                uploadStatus.textContent = "";
            });

            xhr.upload.addEventListener("progress", (e) => {
                if (!e.lengthComputable) return;
                setProgress(e.loaded / e.total);
            });

            xhr.addEventListener("readystatechange", () => {
                if (xhr.readyState !== XMLHttpRequest.DONE) return;
                resetState();

                if (xhr.status >= 200 && xhr.status < 300) {
                    setProgress(1);
                    uploadStatus.textContent = "\u0622\u067E\u0644\u0648\u062F \u0645\u0648\u0641\u0642 \u0628\u0648\u062F\u061B \u062F\u0631 \u062D\u0627\u0644 \u0627\u0646\u062A\u0642\u0627\u0644...";
                    try {
                        const data = JSON.parse(xhr.responseText);
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        }
                    } catch {
                        uploadStatus.textContent = "\u067E\u0627\u0633\u062E \u0646\u0627\u0645\u0639\u062A\u0628\u0631 \u0627\u0632 \u0633\u0631\u0648\u0631";
                    }
                    return;
                }

                let message = "\u0622\u067E\u0644\u0648\u062F \u0646\u0627\u0645\u0648\u0641\u0642 \u0628\u0648\u062F. \u0644\u0637\u0641\u0627\u064B \u062F\u0648\u0628\u0627\u0631\u0647 \u062A\u0644\u0627\u0634 \u06A9\u0646\u06CC\u062F.";
                try {
                    const data = JSON.parse(xhr.responseText);
                    if (data.errors?.file) {
                        message = data.errors.file.join(" ");
                    }
                } catch {}

                uploadStatus.textContent = message;
                uploadProgress.classList.add("shake");
                setTimeout(() => uploadProgress.classList.remove("shake"), 420);
            });

            xhr.addEventListener("error", () => {
                resetState();
                uploadStatus.textContent = "\u062E\u0637\u0627 \u062F\u0631 \u0627\u0631\u062A\u0628\u0627\u0637 \u0628\u0627 \u0633\u0631\u0648\u0631";
            });

            xhr.send(formData);
        });
    };

    doc.addEventListener("DOMContentLoaded", () => {
        body.classList.remove("no-js");
        detectLiteMode();
        initPreloader();
        initTabs();
        initCopyButtons();
        initThemeToggle();
        initTopbarScroll();
        initPressFeedback();
        initRevealObserver();
        const flashApi = initFlashMessages();
        initUploadForm(flashApi?.pushFlash);
    });
})();

