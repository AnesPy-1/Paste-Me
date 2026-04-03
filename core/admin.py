from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import PasteItem, SiteSetting, Wallet


@admin.register(PasteItem)
class PasteItemAdmin(admin.ModelAdmin):
    """Admin interface for PasteItem with organized display and filtering."""

    list_display = ("code", "get_item_type", "created_at", "content_preview")
    list_filter = ("created_at",)
    search_fields = ("code", "content")
    readonly_fields = ("code", "created_at", "file_info")
    list_display_links = ("code",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    
    fieldsets = (
        (_("محتوا"), {"fields": ("code", "content", "file", "file_info")}),
        (_("اطلاعات"), {"fields": ("created_at",)}),
    )

    def get_item_type(self, obj):
        """Display whether item is text or file."""
        return _("متن") if obj.is_text else _("فایل")
    get_item_type.short_description = _("نوع")
    
    def content_preview(self, obj):
        """Display preview of content or filename."""
        if obj.is_text:
            preview = obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
            return preview
        else:
            return obj.file_name or "-"
    content_preview.short_description = _("پیش‌نمایش")
    
    def file_info(self, obj):
        """Display file information if available."""
        if obj.file:
            size_kb = obj.file.size / 1024
            return f"{obj.file_name} ({size_kb:.2f} KiB)"
        return "-"
    file_info.short_description = _("اطلاعات فایل")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    """Admin interface for site-wide settings."""

    list_display = ("is_visible", "updated_at")
    readonly_fields = ("updated_at",)
    
    fieldsets = (
        (_("عمومی"), {"fields": ("is_visible",)}),
        (_("برندینگ"), {"fields": ("brand_logo", "brand_icon")}),
        (_("حمایت"), {"fields": ("reymit_link",)}),
        (_("سازنده"), {"fields": ("author_username", "author_url")}),
        (_("اطلاعات"), {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        """Allow only one SiteSetting instance."""
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the single SiteSetting instance."""
        return False


# Wallet admin commented out - using only Reymit link in SiteSetting
# @admin.register(Wallet)
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ("get_network_display", "address_preview", "description", "order", "is_active")
#     list_filter = ("network", "is_active", "created_at")
#     search_fields = ("address", "description")
#     ordering = ("order", "-created_at")
#     fieldsets = (
#         (None, {"fields": ("network", "address", "description")}),
#         (_("تنظیمات"), {"fields": ("order", "is_active")}),
#         (_("زمان"), {"fields": ("created_at",), "classes": ("collapse",)}),
#     )
#     readonly_fields = ("created_at",)
#
#     def address_preview(self, obj):
#         preview = obj.address[:30] + "..." if len(obj.address) > 30 else obj.address
#         return preview
#     address_preview.short_description = "آدرس"


# Admin panel customization
admin.site.site_header = "مدیریت پیست‌می"
admin.site.site_title = "پنل مدیریت"
admin.site.index_title = "داشبورد ادمین"
