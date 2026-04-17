from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from . import keep_views

app_name = "myapp"

urlpatterns = [
    # =========================
    # トップ・基本ページ
    # =========================
    path('', keep_views.IndexView.as_view(), name='index'),          # トップページ
    path('about/', keep_views.AboutView.as_view(), name='about'),    # Aboutページ

    # =========================
    # MyApp 本体（CRUD）
    # =========================
    path('list/', keep_views.myappListView, name='list'),            # 投稿一覧ページ
    path('detail/<int:pk>/', keep_views.myappDetailView, name='detail'),  # 投稿詳細
    path('form/', login_required(keep_views.myappCreateView), name='form'),  # 投稿作成フォーム
    path('update/<int:pk>/', login_required(keep_views.myappUpdateView), name='update'),  # 投稿更新
    path('delete/<int:pk>/', login_required(keep_views.myappDeleteView), name='delete'),  # 投稿削除

    # =========================
    # Person
    # =========================
    path('person_list/', login_required(keep_views.PersonListView.as_view()), name='person_list'),
    # =========================
    # 認証
    # =========================
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('loggedin/', keep_views.loggedin_view, name='loggedin'),

    # =========================
    # MyMail
    # =========================
    path('mymail/form/', keep_views.mymailCreateView, name='mymail_form'),
    path('mymail/list/', keep_views.mymail_list, name='mymail_list'),
]
