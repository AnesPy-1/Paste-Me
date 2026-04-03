# Generated migration: rename remit_link to reymit_link

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_wallet_sitesetting_remit_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesetting',
            old_name='remit_link',
            new_name='reymit_link',
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='reymit_link',
            field=models.URLField(blank=True, help_text='لینک حساب Reymit شما برای پذیرش پرداخت', verbose_name='لینک Reymit'),
        ),
    ]
