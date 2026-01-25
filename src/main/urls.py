from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # トップ / About（myapp.viewsに依存しない）
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),

    # サインアップ（必要なら myapp 側へ委譲）
    path("accounts/signup/", TemplateView.as_view(template_name="registration/signup.html"), name="signup"),
    # ※もし signup_view を使うなら下の行にして、上の TemplateView 行は消す
    # from myapp import views as myapp_views
    # path("accounts/signup/", myapp_views.signup_view, name="signup"),

    # Django標準 認証（login / logout / password）
    path("accounts/", include("django.contrib.auth.urls")),

    # myapp
    path("myapp/", include("myapp.urls")),
]

