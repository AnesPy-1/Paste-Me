from django.conf import settings
from django.contrib import messages
from django.core.exceptions import RequestDataTooBig
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views.generic import DetailView, FormView, TemplateView, View

from .forms import CodeLookupForm, FileUploadForm, TextPasteForm
from .models import PasteItem


class HomeView(TemplateView):
    template_name = "home.html"
    allowed_panels = {"text-panel", "file-panel", "lookup-panel"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_panel = kwargs.get("active_panel") or self.request.GET.get("panel")
        if requested_panel not in self.allowed_panels:
            requested_panel = "text-panel"
        context["text_form"] = kwargs.get("text_form", TextPasteForm())
        context["file_form"] = kwargs.get("file_form", FileUploadForm())
        context["lookup_form"] = kwargs.get("lookup_form", CodeLookupForm())
        context["active_panel"] = requested_panel
        context["max_upload_size"] = settings.MAX_UPLOAD_SIZE
        return context


def render_home(request, **kwargs):
    """Render the home page with provided form/context overrides."""
    context = HomeView().get_context_data(**kwargs)
    return render(request, HomeView.template_name, context)


class TextCreateView(FormView):
    form_class = TextPasteForm
    http_method_names = ["post"]

    def form_valid(self, form):
        item = PasteItem.objects.create(content=form.cleaned_data["content"])
        messages.success(self.request, "متن با موفقیت ذخیره شد.")
        return redirect("result", code=item.code)

    def form_invalid(self, form):
        if form.errors.get("content"):
            messages.error(self.request, form.errors["content"][0])
        return render_home(self.request, text_form=form, active_panel="text-panel")


class FileCreateView(FormView):
    form_class = FileUploadForm
    http_method_names = ["post"]
    oversize_message = "حجم فایل بیشتر از ۲۰۰ مگابایت است. لطفاً فایل کوچک‌تری انتخاب کنید."

    @staticmethod
    def is_ajax(request):
        return request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except RequestDataTooBig:
            if self.is_ajax(request):
                return JsonResponse(
                    {"ok": False, "errors": {"file": [self.oversize_message]}},
                    status=413,
                )
            messages.error(request, self.oversize_message)
            return redirect(f"{reverse('home')}?panel=file-panel")

    def form_valid(self, form):
        item = PasteItem.objects.create(file=form.cleaned_data["file"])
        if self.is_ajax(self.request):
            return JsonResponse(
                {
                    "ok": True,
                    "redirect_url": reverse("result", kwargs={"code": item.code}),
                    "code": item.code,
                },
                status=201,
            )
        messages.success(self.request, "فایل با موفقیت آپلود شد.")
        return redirect("result", code=item.code)

    def form_invalid(self, form):
        error_message = form.errors.get("file", ["آپلود ناموفق بود."])[0]
        if self.is_ajax(self.request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(self.request, error_message)
        return render_home(self.request, file_form=form, active_panel="file-panel")


class LookupRedirectView(FormView):
    form_class = CodeLookupForm
    http_method_names = ["post"]

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        try:
            PasteItem.objects.get(code=code)
        except PasteItem.DoesNotExist:
            raise Http404()
        return redirect("item-detail", code=code)

    def form_invalid(self, form):
        if form.errors.get("code"):
            messages.error(self.request, form.errors["code"][0])
        return render_home(self.request, lookup_form=form, active_panel="lookup-panel")


class ResultView(DetailView):
    template_name = "result.html"
    model = PasteItem
    slug_field = "code"
    slug_url_kwarg = "code"
    context_object_name = "item"


class PasteItemDetailView(DetailView):
    template_name = "item_detail.html"
    model = PasteItem
    slug_field = "code"
    slug_url_kwarg = "code"
    context_object_name = "item"


class FileDownloadView(View):
    http_method_names = ["get"]

    def get(self, request, code):
        try:
            item = PasteItem.objects.get(code=code, file__isnull=False)
        except PasteItem.DoesNotExist:
            raise Http404()

        if not item.file:
            raise Http404()

        safe_name = get_valid_filename(item.file_name) or "download"
        response = FileResponse(item.file.open("rb"), as_attachment=True, filename=safe_name)
        response["Content-Type"] = "application/octet-stream"
        if item.file and hasattr(item.file, "size"):
            response["Content-Length"] = item.file.size
        return response


class RobotsTxtView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if not settings.SEARCH_INDEXABLE:
            content = "User-agent: *\nDisallow: /\n"
            return HttpResponse(content, content_type="text/plain; charset=utf-8")

        admin_path = settings.ADMIN_URL_PATH.strip("/")
        sitemap_url = request.build_absolute_uri(reverse("sitemap"))
        lines = [
            "User-agent: *",
            "Allow: /",
            f"Disallow: /{admin_path}/",
            "Disallow: /paste/",
            "Disallow: /upload/",
            "Disallow: /view/",
            "Disallow: /result/",
            "Disallow: /item/",
            "Disallow: /download/",
            f"Sitemap: {sitemap_url}",
        ]
        return HttpResponse("\n".join(lines) + "\n", content_type="text/plain; charset=utf-8")
