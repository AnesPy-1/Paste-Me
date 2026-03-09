from django.http import HttpResponse
from django.shortcuts import redirect
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


class TextCreateView(FormView):
    form_class = TextPasteForm
    http_method_names = ["post"]

    def form_valid(self, form):
        item = PasteItem.objects.create(content=form.cleaned_data["content"])
        return redirect("result", code=item.code)

    def form_invalid(self, form):
        return HomeView.as_view()(self.request, text_form=form, active_panel="text-panel")


class FileCreateView(FormView):
    form_class = FileUploadForm
    http_method_names = ["post"]

    def form_valid(self, form):
        item = PasteItem.objects.create(file=form.cleaned_data["file"])
        return redirect("result", code=item.code)

    def form_invalid(self, form):
        return HomeView.as_view()(self.request, file_form=form, active_panel="file-panel")


class LookupRedirectView(FormView):
    form_class = CodeLookupForm
    http_method_names = ["post"]

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        if not PasteItem.objects.filter(code=code).exists():
            form.add_error("code", "محتوایی با این کد پیدا نشد.")
            return self.form_invalid(form)
        return redirect("item-detail", code=code)

    def form_invalid(self, form):
        return HomeView.as_view()(self.request, lookup_form=form, active_panel="lookup-panel")


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


class RobotsTxtView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return HttpResponse("User-agent: *\nDisallow: /\n", content_type="text/plain; charset=utf-8")
