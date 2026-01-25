from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "myapp"

urlpatterns = [
    # /myapp/ の入口
    path("", views.person_list, name="root"),

    path("person_list/", views.person_list, name="person_list"),

    path("list/", TemplateView.as_view(template_name="index.html")),
    path("detail/", views.myapp_detail_latest, name="detail_latest"),
    path("detail/<int:pk>/", views.myappDetailView, name="detail"),
    path("form/", views.myappCreateView, name="form"),
    path("update/<int:pk>/", views.myappUpdateView, name="update"),
    path("delete/<int:pk>/", views.myappDeleteView, name="delete"),

    path("mymail/", views.mymailCreateView, name="mymail"),
    path("mymail_list/", views.mymail_list, name="mymail_list"),

    # 一般ユーザー登録
    path("signup/", views.signup_view, name="signup"),

    # 一般ユーザー専用ページ
    path("dashboard/", views.user_dashboard, name="dashboard"),
]
