# pasteme

pasteme یک وب‌اپلیکیشن سبک و production-ready برای اشتراک متن و فایل با کد ۶ رقمی است. این پروژه با Django و SQLite ساخته شده و بدون سیستم احراز هویت، مسیر ساده‌ای برای ذخیره و بازیابی محتوا ارائه می‌دهد.

## Features

- پیست متن و دریافت کد ۶ رقمی یکتا
- آپلود فایل با محدودیت ۱۰ مگابایت
- مشاهده متن یا فایل با استفاده از کد
- دانلود فایل و کپی محتوا با JavaScript
- رابط کاربری فارسی، مینیمال و responsive

## Screenshots

- Placeholder: Home page
- Placeholder: Result page
- Placeholder: Item detail page

## Live Preview

https://pasteme.site

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript

## Installation Guide

```bash
git clone <repository-url>
cd pasteme
python manage.py migrate
python manage.py runserver
```

## Run Instructions

1. نصب وابستگی‌ها:
   `pip install django`
2. اجرای مایگریشن‌ها:
   `python manage.py migrate`
3. اجرای سرور:
   `python manage.py runserver`
4. باز کردن آدرس:
   `http://127.0.0.1:8000`

## Folder Structure

```text
pasteme/
├── core/
├── pasteme/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py
└── README.md
```

## Recommended Commit Messages

- `feat: add paste text feature`
- `feat: implement file upload`
- `feat: add code retrieval system`
- `style: improve UI layout`
- `docs: add project README`

## Author

AnesPy
