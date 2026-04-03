from django.urls import path

from .views import (
    DonationView,
    FileCreateView,
    FileDownloadView,
    HomeView,
    LookupRedirectView,
    PasteItemDetailView,
    ResultView,
    TextCreateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("paste/", TextCreateView.as_view(), name="paste-text"),
    path("upload/", FileCreateView.as_view(), name="upload-file"),
    path("download/<slug:code>/", FileDownloadView.as_view(), name="download-file"),
    path("view/", LookupRedirectView.as_view(), name="lookup"),
    path("result/<slug:code>/", ResultView.as_view(), name="result"),
    path("item/<slug:code>/", PasteItemDetailView.as_view(), name="item-detail"),
    path("donation/", DonationView.as_view(), name="donation"),
]
