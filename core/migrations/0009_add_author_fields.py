# Generated migration: add author fields to SiteSetting

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_remit_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='author_username',
            field=models.CharField(default='AnesPy', help_text='مثال: @AnesPy (بدون نماد @)', max_length=50, verbose_name='نام کاربری سازنده'),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='author_url',
            field=models.URLField(default='https://t.me/AnesPy', help_text='URL پروفایل یا صفحه شخصی سازنده', verbose_name='لینک پروفایل سازنده'),
        ),
    ]
