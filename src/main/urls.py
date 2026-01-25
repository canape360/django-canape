from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # トップとAboutはテンプレ直指定（myapp.viewsに依存しない）
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),

    # 認証
    path("accounts/", include("django.contrib.auth.urls")),

    # myapp
    path("myapp/", include("myapp.urls")),
]
