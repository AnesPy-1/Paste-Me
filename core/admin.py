from django.contrib import admin

from .models import PasteItem, SiteSetting


@admin.register(PasteItem)
class PasteItemAdmin(admin.ModelAdmin):
    list_display = ("code", "created_at", "content", "file")
    search_fields = ("code", "content")
    readonly_fields = ("code", "created_at")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("is_visible", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
