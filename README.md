# PasteMe
ابزار متن‌باز اشتراک‌گذاری متن یا فایل با کد شش‌رقمی، رابط فارسی، و تم روشن/تاریک. همه‌ی فونت و استایل‌ها لوکال هستند و برای دیپلوی پشت فایروال/بدون اینترنت بیرونی مناسب است.

## ویژگی‌ها
- پیست متن یا آپلود فایل تا ۲۰۰ مگابایت و دریافت کد یکتا
- دانلود امن با نام فایل سالم‌سازی‌شده و پشتیبانی از `Content-Length`
- `sitemap.xml` و `robots.txt` داینامیک برای کنترل ایندکس موتورهای جست‌وجو
- سوییچ تم روشن/تاریک، رابط RTL بهینه برای موبایل، هدر/فوتر فیکس
- قفل دسترسی با `PUBLIC_HOSTS` و صفحه‌ی «سایت بسته است» از طریق `SiteSetting`
- مسیر ادمین قابل تنظیم (پیش‌فرض: `/pasteme-admin/`) و برندینگ لوگو/فاوآیکن از پنل

## پیش‌نیاز
- Python 3.11+
- pip و virtualenv

## نصب و راه‌اندازی سریع
```bash
git clone <repo>
cd PasteMe
python -m venv .venv
. .venv/Scripts/activate  # یا source .venv/bin/activate در لینوکس/مک
pip install -r requirements.txt
cp .env.example .env  # مقادیر را ویرایش کنید
python manage.py migrate
python manage.py runserver
```

## پیکربندی محیطی
فایل `.env` را بر اساس `.env.example` تنظیم کنید:

- `DJANGO_DEBUG`: برای تولید `False`
- `DJANGO_SECRET_KEY`: کلید قوی و محرمانه
- `DJANGO_ALLOWED_HOSTS`: لیست هاست‌های مجاز (کاما جدا)
- `DJANGO_PUBLIC_HOSTS`: هاست‌هایی که اجازه‌ی دسترسی عمومی دارند
- `DJANGO_CSRF_TRUSTED_ORIGINS`: ریشه‌های مجاز CSRF (با `https://`)
- `DJANGO_ADMIN_PATH`: مسیر پنل مدیریت (مثال: `pasteme-admin/`)
- `DJANGO_SEARCH_INDEXABLE`: فعال/غیرفعال کردن ایندکس موتورهای جست‌وجو

## دستورهای معمول
- اجرای تست‌ها: `python manage.py test`
- جمع‌آوری استاتیک: `python manage.py collectstatic`
- ساخت ادمین: `python manage.py createsuperuser`

## نکات امنیت و دیپلوی
- در تولید حتماً `DJANGO_DEBUG=False` و `DJANGO_SECRET_KEY` تصادفی باشد.
- هدرهای امنیتی (HSTS، Secure cookies) بر اساس DEBUG تنظیم می‌شوند.
- `PUBLIC_HOSTS` را فقط روی دامنه‌های واقعی خود بگذارید؛ بقیه درخواست‌ها 403 می‌گیرند.
- حداکثر حجم آپلود ۲۰۰ مگابایت است؛ در صورت نیاز به بیشتر، مقدار `FILE_UPLOAD_MAX_MEMORY_SIZE` را تغییر دهید.
- فایل‌ها در `media/` ذخیره می‌شوند؛ دسترسی عمومی را فقط روی مسیر `/media/` بخوانید.

## تست‌ها
۱۳ تست واحد با Django TestCase پوشش می‌دهند:
- اعتبارسنجی مدل و تولید کد یکتا
- ویژگی‌های فایل/تصویر
- فرم‌ها و ویوهای پیست متن و آپلود فایل
- ریدایرکت و دانلود فایل با هدر صحیح
- میان‌افزارهای PublicHost، SiteVisibility، و NoIndex

## لایسنس
MIT – آزادید فورک کنید و بهبود دهید. اگر استفاده کردید، خوشحال می‌شوم خبر بدهید.
