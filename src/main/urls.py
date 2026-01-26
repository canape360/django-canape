# main/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from myapp import views as myapp_views  # ✅ 追加

urlpatterns = [
    path("admin/", admin.site.urls),

    # トップ / About
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),

    # ✅ サインアップは view で処理する（TemplateViewは使わない）
    path("accounts/signup/", myapp_views.signup_view, name="signup"),

    # Django標準 認証（login / logout / password）
    path("accounts/", include("django.contrib.auth.urls")),

    # diaryapp
    path("diary/", include("diaryapp.urls")),

    # myapp
    path("myapp/", include("myapp.urls")),
]
