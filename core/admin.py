from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import PasteItem, SiteSetting


@admin.register(PasteItem)
class PasteItemAdmin(admin.ModelAdmin):
    list_display = ("code", "created_at", "content", "file")
    search_fields = ("code", "content")
    readonly_fields = ("code", "created_at")
    list_display_links = ("code",)
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("code", "content", "file")}),
        (_("زمان"), {"fields": ("created_at",)}),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("is_visible", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "مدیریت پیست‌می"
admin.site.site_title = "پنل مدیریت"
admin.site.index_title = "داشبورد ادمین"
