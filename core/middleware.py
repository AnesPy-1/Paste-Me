from django.conf import settings
from django.db import OperationalError, ProgrammingError
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import SiteSetting


class PublicHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        is_exempt_path = (
            request.path.startswith("/admin/")
            or request.path.startswith("/static/")
            or request.path.startswith("/media/")
        )
        if not is_exempt_path and host not in settings.PUBLIC_HOSTS:
            return HttpResponseForbidden("Access denied.")
        return self.get_response(request)


class SiteVisibilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        try:
            if not SiteSetting.load().is_visible:
                return render(request, "site_closed.html", status=503)
        except (OperationalError, ProgrammingError):
            pass

        return self.get_response(request)


class NoIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Robots-Tag"] = "noindex, nofollow, noarchive, nosnippet, noimageindex"
        return response
