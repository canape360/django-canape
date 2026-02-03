import os
import traceback

from django.urls import path
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import connection

from . import views

app_name = "myapp"

# Render / 本番でだけ debug を出すかどうかを環境変数で制御（Renderの環境変数で ON にできる）
DEBUG_ENDPOINTS = os.environ.get("DEBUG_ENDPOINTS", "0") == "1"
# urls.py（DEBUG_ENDPOINTS=1のときだけ有効にしている前提）

def table_schema(request, table):
    if not _debug_guard(request):
        return HttpResponseForbidden("debug endpoint disabled")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, [table])
        rows = cursor.fetchall()

    return JsonResponse({
        "table": table,
        "columns": [{"name": r[0], "type": r[1], "nullable": r[2]} for r in rows],
    })



def health(request):
    commit = os.environ.get("RENDER_GIT_COMMIT", "unknown")
    return HttpResponse(f"ok commit={commit}")


def dbcheck(request):
    return JsonResponse({
        "vendor": connection.vendor,
        "tables": connection.introspection.table_names(),
    })


def migcheck(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT app, name, applied
            FROM django_migrations
            WHERE app = 'myapp'
            ORDER BY applied;
        """)
        rows = cursor.fetchall()

    return JsonResponse({
        "myapp_migrations": [
            {"app": r[0], "name": r[1], "applied": str(r[2])} for r in rows
        ]
    })


def _debug_guard(request):
    # 本番公開中は危険なので、環境変数がONのときだけ許可
    if not DEBUG_ENDPOINTS:
        return False
    # さらに安全にするならログイン必須や staff 限定にする（必要ならここで追加）
    return True


def list_debug(request):
    if not _debug_guard(request):
        return HttpResponseForbidden("debug endpoint disabled")
    try:
        return views.myappListView(request)
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(f"<pre>{tb}</pre>", status=500)


def form_debug(request):
    if not _debug_guard(request):
        return HttpResponseForbidden("debug endpoint disabled")
    try:
        return views.myappCreateView(request)
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(f"<pre>{tb}</pre>", status=500)


def detail_latest_debug(request):
    if not _debug_guard(request):
        return HttpResponseForbidden("debug endpoint disabled")
    try:
        return views.myapp_detail_latest(request)
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(f"<pre>{tb}</pre>", status=500)
def diary_schema(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'myapp_diary'
            ORDER BY ordinal_position;
        """)
        cols = cursor.fetchall()

    return JsonResponse({
        "table": "myapp_diary",
        "columns": [{"name": c[0], "type": c[1], "nullable": c[2]} for c in cols]
    })


urlpatterns = [
    # 疎通確認
    path("health/", health, name="health"),
    path("dbcheck/", dbcheck, name="dbcheck"),
    path("migcheck/", migcheck, name="migcheck"),

    # debug（本番公開中は DEBUG_ENDPOINTS=1 の時だけ有効）
    path("list-debug/", list_debug, name="list_debug"),
    path("form-debug/", form_debug, name="form_debug"),
    path("detail-latest-debug/", detail_latest_debug, name="detail_latest_debug"),

    # /myapp/ の入口
    path("", views.person_list, name="root"),
    path("person_list/", views.person_list, name="person_list"),
    path("person/<int:pk>/", views.person_detail, name="person_detail"),

    

    # CRUD
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

    path("diary-schema/", diary_schema, name="diary_schema"),
    path("table-schema/<str:table>/", table_schema, name="table_schema"),

]

# django-canape/src/myapp/urls.py