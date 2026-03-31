import random

from django.core.exceptions import ValidationError
from django.db import models


def upload_to(instance, filename):
    return f"uploads/{instance.code}/{filename}"


class PasteItem(models.Model):
    code = models.CharField("کد", max_length=6, unique=True, editable=False)
    content = models.TextField("متن", blank=True, null=True)
    file = models.FileField("فایل", upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "مورد پیست"
        verbose_name_plural = "موردهای پیست"
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    @property
    def is_text(self):
        return bool(self.content)

    @property
    def file_name(self):
        return self.file.name.rsplit("/", 1)[-1] if self.file else ""

    @property
    def is_image(self):
        if not self.file:
            return False
        ext = self.file_name.rsplit(".", 1)[-1].lower() if "." in self.file_name else ""
        return ext in {"png", "jpg", "jpeg", "gif", "webp", "bmp"}

    def clean(self):
        if bool(self.content) == bool(self.file):
            raise ValidationError("Only one of content or file must be set.")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def generate_unique_code(cls):
        for _ in range(50):
            code = f"{random.randint(0, 999999):06d}"
            if not cls.objects.filter(code=code).exists():
                return code
        raise RuntimeError("Could not generate a unique 6-digit code.")

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


class SiteSetting(models.Model):
    is_visible = models.BooleanField(default=True, verbose_name="نمایش سایت")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تنظیم سایت"
        verbose_name_plural = "تنظیم سایت"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
