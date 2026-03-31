from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import get_valid_filename
from django.views.generic import DetailView, FormView, TemplateView, View

from .forms import CodeLookupForm, FileUploadForm, TextPasteForm
from .models import PasteItem


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_form"] = kwargs.get("text_form", TextPasteForm())
        context["file_form"] = kwargs.get("file_form", FileUploadForm())
        context["lookup_form"] = kwargs.get("lookup_form", CodeLookupForm())
        context["active_panel"] = kwargs.get("active_panel", "text-panel")
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
        return redirect("result", code=item.code)

    def form_invalid(self, form):
        return render_home(self.request, text_form=form, active_panel="text-panel")


class FileCreateView(FormView):
    form_class = FileUploadForm
    http_method_names = ["post"]

    def form_valid(self, form):
        item = PasteItem.objects.create(file=form.cleaned_data["file"])
        return redirect("result", code=item.code)

    def form_invalid(self, form):
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
        return response


class RobotsTxtView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return HttpResponse("User-agent: *\nDisallow: /\n", content_type="text/plain; charset=utf-8")
