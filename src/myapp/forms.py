from django import forms
from .models import MyApp, MyMail


# =========================
# MyApp 用フォーム（日記）
# =========================
class MyAppForm(forms.ModelForm):
    class Meta:
        model = MyApp
        fields = ["title", "body"]  # ★ content → body
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "タイトルを入力",
            }),
            "body": forms.Textarea(attrs={  # ★ content → body
                "class": "form-control",
                "rows": 12,
                "placeholder": "日記の内容を入力してください",
            }),
        }


# =========================
# MyMail 用フォーム（保存）
# =========================
class MyMailForm(forms.ModelForm):
    class Meta:
        model = MyMail
        fields = ["subject", "message", "sender"]
        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "件名",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "お問い合わせ内容",
            }),
            "sender": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "メールアドレス",
            }),
        }


# =========================
# MyMail 用フォーム（検索専用）
# =========================
class MyMailSearchForm(forms.Form):
    search = forms.CharField(
        label="検索",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "件名・本文で検索",
        }),
    )
