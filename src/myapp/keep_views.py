from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.asgi import get_asgi_application

from .models import MyApp, Person, MyMail
from .forms import MyAppForm, MyMailForm
from .forms import MyMailSearchForm  # ← 検索専用フォーム


# =========================
# 共通ページ
# =========================
class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


def index(request):
    return render(request, "index.html")


def form_view(request):
    return render(request, "myapp/form.html")


def loggedin_view(request):
    return render(request, 'loggedin_template.html', {
        'message': 'ログインしました。ようこそ！',
    })


# =========================
# Person
# =========================
@login_required
def person_list(request):
    data = Person.objects.all()
    return render(request, 'person_list.html', {'data': data})


class PersonListView(ListView):
    model = Person


# =========================
# MyApp（CRUD）
# =========================
def myappListView(request):
    objects = MyApp.objects.all()
    return render(request, "myapp/myapp_list.html", {
        "object_list": objects
    })


def myappDetailView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)
    return render(request, "myapp/myapp-detail.html", {
        "object": obj
    })


def myappCreateView(request):
    if request.method == "POST":
        form = MyAppForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('myapp:detail', pk=obj.pk)
    else:
        form = MyAppForm()

    return render(request, "myapp/myapp_form.html", {
        "form": form
    })


def myappUpdateView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)

    if request.method == "POST":
        form = MyAppForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('myapp:detail', pk=obj.pk)
    else:
        form = MyAppForm(instance=obj)

    return render(request, 'myapp/myapp_update.html', {
        'form': form,
        'object': obj,
    })


def myappDeleteView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("myapp:list")

    return render(request, "myapp/delete_template.html", {
        "object": obj,
    })


# =========================
# MyMail
# =========================
def mymailCreateView(request):
    if request.method == "POST":
        form = MyMailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'メールを送信しました')
            return redirect("myapp:mymail_list")
    else:
        form = MyMailForm()

    return render(request, "myapp/mymail-form.html", {
        "form": form,
    })


def mymail_list(request):
    search_form = MyMailSearchForm(request.GET)
    objects = MyMail.objects.all()

    if search_form.is_valid():
        search_term = search_form.cleaned_data.get('search')
        if search_term:
            objects = objects.filter(subject__icontains=search_term)

    return render(request, 'myapp/mymail_list.html', {
        'object_list': objects,
        'search_form': search_form,
    })


# =========================
# ASGI lifecycle
# =========================
from .my_custom_startup_handler import my_custom_startup_handler
from .my_custom_shutdown_handler import my_custom_shutdown_handler

django_asgi_app = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'lifespan':
        if scope['asgi']['type'] == 'startup':
            await my_custom_startup_handler()
        elif scope['asgi']['type'] == 'shutdown':
            await my_custom_shutdown_handler()
    else:
        await django_asgi_app(scope, receive, send)
