import os
import traceback

from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.db import connection

from . import views

app_name = "myapp"


def health(request):
    commit = os.environ.get("RENDER_GIT_COMMIT", "unknown")
    return HttpResponse(f"ok commit={commit}")


def dbcheck(request):
    return JsonResponse({
        "vendor": connection.vendor,
        "tables": connection.introspection.table_names(),
    })


def list_debug(request):
    try:
        return views.myappListView(request)
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(f"<pre>{tb}</pre>", status=500)


urlpatterns = [
    # 疎通確認
    path("health/", health, name="health"),
    path("dbcheck/", dbcheck, name="dbcheck"),

    # ★ これが無かった（超重要）
    path("list-debug/", list_debug, name="list_debug"),

    # /myapp/ の入口
    path("", views.person_list, name="root"),
    path("person_list/", views.person_list, name="person_list"),

    # MyApp CRUD
    path("list/", views.myappListView, name="list"),
    path("detail/", views.myapp_detail_latest, name="detail_latest"),
    path("detail/<int:pk>/", views.myappDetailView, name="detail"),
    path("form/", views.myappCreateView, name="form"),
    path("update/<int:pk>/", views.myappUpdateView, name="update"),
    path("delete/<int:pk>/", views.myappDeleteView, name="delete"),

    # MyMail
    path("mymail/", views.mymailCreateView, name="mymail"),
    path("mymail_list/", views.mymail_list, name="mymail_list"),

    # signup / dashboard
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.user_dashboard, name="dashboard"),
]
