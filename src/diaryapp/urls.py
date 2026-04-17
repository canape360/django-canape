#diaryapp/urls.py（作成 or 置き換え）
from django.urls import path
from . import views

app_name = "diaryapp"

urlpatterns = [
    # ✅ 公開（ログイン不要）
    path("public/", views.PublicDiaryListView.as_view(), name="public_list"),
    path("public/<int:pk>/", views.PublicDiaryDetailView.as_view(), name="public_detail"),

    # ✅ 自分用（ログイン必須）
    path("", views.DiaryListView.as_view(), name="list"),
    path("create/", views.DiaryCreateView.as_view(), name="create"),
    path("<int:pk>/", views.DiaryDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.DiaryUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DiaryDeleteView.as_view(), name="delete"),
]
