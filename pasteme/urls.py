from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import RobotsTxtView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
