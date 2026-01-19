
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('person_list/', views.person_list, name='person_list'),

    path('list/', views.myappListView, name='list'),
    path('detail/<int:pk>/', views.myappDetailView, name='detail'),
    path('form/', views.myappCreateView, name='form'),
    path('update/<int:pk>/', views.myappUpdateView, name='update'),
    path('delete/<int:pk>/', views.myappDeleteView, name='delete'),

    path('mymail/', views.mymailCreateView, name='mymail'),
    path('mymail_list/', views.mymail_list, name='mymail_list'),

    # 一般ユーザー登録
    path("signup/", views.signup_view, name="signup"),
    path("person_list/", views.person_list, name="person_list"),

    # 一般ユーザー専用ページ
    path("dashboard/", views.user_dashboard, name="dashboard"),
]

