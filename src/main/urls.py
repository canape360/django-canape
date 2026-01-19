from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import IndexView, AboutView, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # トップページ
    path('', IndexView.as_view(), name='index'),

    # ✅ 一般ユーザー登録
    path('accounts/signup/', signup_view, name='signup'),

    # Django標準 認証（login / logout / password）
    path('accounts/', include('django.contrib.auth.urls')),

    # myapp（業務・一般ユーザー）
    path('myapp/', include('myapp.urls')),

    # About
    path('about/', AboutView.as_view(), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
