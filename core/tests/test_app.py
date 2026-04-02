import shutil
import tempfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse

from core.middleware import NoIndexMiddleware, PublicHostMiddleware, SiteVisibilityMiddleware
from core.models import PasteItem, SiteSetting


class MediaRootTestCase(TestCase):
    def setUp(self):
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.temp_media, ignore_errors=True))


@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1024 * 1024, MEDIA_ROOT=tempfile.gettempdir())
class PasteItemModelTests(TestCase):
    def test_clean_rejects_both_or_neither(self):
        with self.assertRaises(ValidationError):
            PasteItem(content="text", file=SimpleUploadedFile("f.txt", b"data")).full_clean()
        with self.assertRaises(ValidationError):
            PasteItem().full_clean()

    def test_generate_unique_code_is_six_digits(self):
        item = PasteItem.objects.create(content="hello")
        self.assertEqual(len(item.code), 6)
        self.assertTrue(item.code.isdigit())

    def test_is_text_property(self):
        item = PasteItem.objects.create(content="sample")
        self.assertTrue(item.is_text)
        item_file = PasteItem.objects.create(file=SimpleUploadedFile("f.txt", b"file"))
        self.assertFalse(item_file.is_text)

    def test_is_image_property(self):
        png = PasteItem.objects.create(file=SimpleUploadedFile("pic.png", b"img"))
        self.assertTrue(png.is_image)
        txt = PasteItem.objects.create(file=SimpleUploadedFile("doc.txt", b"txt"))
        self.assertFalse(txt.is_image)


class FormAndViewTests(MediaRootTestCase):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_HOST="localhost")

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_text_create_view_creates_item(self):
        resp = self.client.post(reverse("paste-text"), {"content": "hello world"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(PasteItem.objects.filter(content="hello world").exists())

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_file_create_view_uploads_file(self):
        file_obj = SimpleUploadedFile("test.bin", b"\x00\x01")
        resp = self.client.post(reverse("upload-file"), {"file": file_obj})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(PasteItem.objects.count(), 1)
        self.assertTrue(PasteItem.objects.first().file)

    def test_lookup_redirect_404_on_missing(self):
        resp = self.client.post(reverse("lookup"), {"code": "123456"})
        self.assertEqual(resp.status_code, 404)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_download_view_serves_file(self):
        item = PasteItem.objects.create(file=SimpleUploadedFile("weird name.bin", b"data"))
        resp = self.client.get(reverse("download-file", kwargs={"code": item.code}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("attachment", resp["Content-Disposition"])
        self.assertEqual(resp["Content-Type"], "application/octet-stream")

    @override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=4, MEDIA_ROOT=tempfile.gettempdir())
    def test_file_upload_form_rejects_large(self):
        big_file = SimpleUploadedFile("big.bin", b"x" * 8)
        resp = self.client.post(reverse("upload-file"), {"file": big_file})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "حجم فایل نباید بیشتر از ۲۰۰ مگابایت باشد.")


class MiddlewareTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(ALLOWED_HOSTS=["evil.com"], PUBLIC_HOSTS=["localhost"])
    def test_public_host_blocks_unknown(self):
        request = self.rf.get("/", HTTP_HOST="evil.com")
        middleware = PublicHostMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 403)

    def test_site_visibility_returns_503_when_closed(self):
        SiteSetting.objects.create(pk=1, is_visible=False)
        request = self.rf.get("/")
        middleware = SiteVisibilityMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 503)

    @override_settings(SEARCH_INDEXABLE=False)
    def test_noindex_header_added(self):
        request = self.rf.get("/")
        middleware = NoIndexMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(
            response["X-Robots-Tag"],
            "noindex, nofollow, noarchive, nosnippet, noimageindex",
        )

    @override_settings(SEARCH_INDEXABLE=True)
    def test_noindex_header_not_added_when_indexable(self):
        request = self.rf.get("/")
        middleware = NoIndexMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertNotIn("X-Robots-Tag", response)
