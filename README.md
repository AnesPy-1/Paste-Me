## PasteMe
یک وب‌اپ ساده برای اشتراک متن یا فایل با کد شش‌رقمی. بدون ثبت‌نام، فارسی، و بدون وابستگی به اینترنت بیرونی (فونت و استایل‌ها لوکال هستند).

### چه می‌کند
- پیست متن و دریافت کد یکتا
- آپلود فایل تا ۱۰۰ مگابایت و نمایش/دانلود امن
- مشاهده با وارد کردن کد؛ برای کد ناموجود، ۴۰۴ می‌دهد
- تم روشن/تاریک و رابط فارسی واکنش‌گرا

### استک
- Backend: Django + SQLite
- Frontend: HTML/CSS/JS
- Font: Vazirmatn (لوکال)

### راه‌اندازی سریع
```bash
git clone <repo>
cd pasteme
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### نکته
- قبل از دیپلوی، `python manage.py collectstatic` را اجرا کنید.
- فایل‌ها در `media/` ذخیره می‌شوند و باید توسط وب‌سرور سرو شوند.
