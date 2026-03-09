from django import forms


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
    file = forms.FileField(label="")

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if uploaded_file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("حجم فایل نباید بیشتر از ۱۰ مگابایت باشد.")
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
