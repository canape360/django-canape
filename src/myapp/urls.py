from django.urls import path
from .views import IndexView, AboutView, signup_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('accounts/signup/', signup_view, name='signup'),
]
