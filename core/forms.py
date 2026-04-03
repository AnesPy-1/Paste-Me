from django import forms
from django.conf import settings


class TextPasteForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "placeholder": "متن خود را اینجا وارد کنید",
            }
        ),
    )


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="انتخاب فایل",
        widget=forms.ClearableFileInput(
            attrs={
                "data-max-size": str(settings.MAX_UPLOAD_SIZE),
                "class": "file-input",
            }
        ),
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if uploaded_file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("حجم فایل نباید بیشتر از ۲۰۰ مگابایت باشد.")
        return uploaded_file


class CodeLookupForm(forms.Form):
    code = forms.RegexField(
        regex=r"^\d{6}$",
        label="",
        error_messages={"invalid": "کد باید ۶ رقم باشد."},
        widget=forms.TextInput(
            attrs={
                "placeholder": "کد را وارد کنید",
                "inputmode": "numeric",
                "maxlength": "6",
            }
        ),
    )
