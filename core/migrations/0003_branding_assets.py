from django.db import migrations, models

import core.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_sitesetting"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesetting",
            name="brand_icon",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=core.models.branding_upload,
                verbose_name="آیکن (favicon)",
                help_text="PNG یا ICO مربعی 64×64 یا بزرگ‌تر برای نمایش آیکن مرورگر.",
            ),
        ),
        migrations.AddField(
            model_name="sitesetting",
            name="brand_logo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=core.models.branding_upload,
                verbose_name="لوگو هدر",
                help_text="بهتر است PNG/SVG با پس‌زمینه شفاف و عرض حداقل 320 پیکسل باشد.",
            ),
        ),
    ]
