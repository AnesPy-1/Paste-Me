"""
Tests for PasteMe application including models, views, forms, and middleware.
"""

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
    """Base test case that provides a temporary media root."""

    def setUp(self):
        self.temp_media = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.temp_media, ignore_errors=True))


@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1024 * 1024, MEDIA_ROOT=tempfile.gettempdir())
class PasteItemModelTests(TestCase):
    """Tests for PasteItem model validation and properties."""

    def test_clean_rejects_both_or_neither(self):
        """Test that a PasteItem must have either content or file, not both or neither."""
        # Both content and file
        with self.assertRaises(ValidationError):
            PasteItem(content="text", file=SimpleUploadedFile("f.txt", b"data")).full_clean()
        # Neither content nor file
        with self.assertRaises(ValidationError):
            PasteItem().full_clean()

    def test_generate_unique_code_is_six_digits(self):
        """Test that generated codes are 6-digit numeric strings."""
        item = PasteItem.objects.create(content="hello")
        self.assertEqual(len(item.code), 6)
        self.assertTrue(item.code.isdigit())

    def test_is_text_property(self):
        """Test the is_text property correctly identifies text vs file items."""
        text_item = PasteItem.objects.create(content="sample")
        self.assertTrue(text_item.is_text)
        
        file_item = PasteItem.objects.create(file=SimpleUploadedFile("f.txt", b"file"))
        self.assertFalse(file_item.is_text)

    def test_is_image_property(self):
        """Test the is_image property correctly identifies image files."""
        png_item = PasteItem.objects.create(file=SimpleUploadedFile("pic.png", b"img"))
        self.assertTrue(png_item.is_image)
        
        txt_item = PasteItem.objects.create(file=SimpleUploadedFile("doc.txt", b"txt"))
        self.assertFalse(txt_item.is_image)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class FormAndViewTests(MediaRootTestCase):
    """Tests for forms and views."""

    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_HOST="localhost")

    def test_text_create_view_creates_item(self):
        """Test that posting text creates a new PasteItem."""
        response = self.client.post(reverse("paste-text"), {"content": "hello world"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PasteItem.objects.filter(content="hello world").exists())

    def test_file_create_view_uploads_file(self):
        """Test that posting a file creates a new PasteItem with file."""
        file_obj = SimpleUploadedFile("test.bin", b"\x00\x01")
        response = self.client.post(reverse("upload-file"), {"file": file_obj})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PasteItem.objects.count(), 1)
        self.assertTrue(PasteItem.objects.first().file)

    def test_lookup_redirect_404_on_missing(self):
        """Test that looking up a non-existent code returns 404."""
        response = self.client.post(reverse("lookup"), {"code": "123456"})
        self.assertEqual(response.status_code, 404)

    def test_download_view_serves_file(self):
        """Test that download view serves file with correct headers."""
        item = PasteItem.objects.create(file=SimpleUploadedFile("weird name.bin", b"data"))
        response = self.client.get(reverse("download-file", kwargs={"code": item.code}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertEqual(response["Content-Type"], "application/octet-stream")

    @override_settings(MEDIA_ROOT=tempfile.gettempdir(), MAX_UPLOAD_SIZE=4)
    def test_file_upload_form_rejects_large(self):
        """Test that oversized files are rejected with appropriate error message."""
        big_file = SimpleUploadedFile("big.bin", b"x" * 8)
        response = self.client.post(reverse("upload-file"), {"file": big_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "حجم فایل نباید بیشتر از ۲۰۰ مگابایت باشد.")


class MiddlewareTests(TestCase):
    """Tests for application middleware."""

    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(ALLOWED_HOSTS=["evil.com"], PUBLIC_HOSTS=["localhost"])
    def test_public_host_blocks_unknown(self):
        """Test that requests from unauthorized hosts are blocked."""
        request = self.rf.get("/", HTTP_HOST="evil.com")
        middleware = PublicHostMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 403)

    def test_site_visibility_returns_503_when_closed(self):
        """Test that site returns 503 when is_visible is False."""
        SiteSetting.objects.create(pk=1, is_visible=False)
        request = self.rf.get("/")
        middleware = SiteVisibilityMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 503)

    @override_settings(SEARCH_INDEXABLE=False)
    def test_noindex_header_added(self):
        """Test that noindex header is added when SEARCH_INDEXABLE is False."""
        request = self.rf.get("/")
        middleware = NoIndexMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(
            response["X-Robots-Tag"],
            "noindex, nofollow, noarchive, nosnippet, noimageindex",
        )

    @override_settings(SEARCH_INDEXABLE=True)
    def test_noindex_header_not_added_when_indexable(self):
        """Test that noindex header is not added when SEARCH_INDEXABLE is True."""
        request = self.rf.get("/")
        middleware = NoIndexMiddleware(lambda req: HttpResponse("ok"))
        response = middleware(request)
        self.assertNotIn("X-Robots-Tag", response)
