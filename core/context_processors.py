from django.conf import settings
from django.db import OperationalError, ProgrammingError

from .models import SiteSetting


def site_settings(request):
    try:
        site_setting = SiteSetting.load()
    except (OperationalError, ProgrammingError):
        site_setting = SiteSetting(is_visible=True)

    return {
        "site_settings": site_setting,
        "search_indexable": settings.SEARCH_INDEXABLE,
        "admin_url_path": settings.ADMIN_URL_PATH,
        "reymit_logo_url": "/static/img/reymit-logo.png",
        "author_mention": f"@{site_setting.author_username}",
        "author_url": site_setting.author_url,
    }
