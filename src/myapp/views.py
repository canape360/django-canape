from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
#from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
#from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from .models import MyApp, Person, MyMail
#from .forms import MyAppForm, MyMailForm, MyMailSearchForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.http import HttpResponse
# views.py 冒頭をこうする（切り分け用）

from django.http import HttpResponse

def myappListView(request):
    return HttpResponse("views loaded OK")


def myapp_detail_latest(request):
    obj = MyApp.objects.order_by("-id").first()
    if not obj:
        return redirect("myapp:list")
    return redirect("myapp:detail", pk=obj.pk)


@login_required
def user_dashboard(request):
    return render(request, "myapp/user_dashboard.html")


# =========================
# 共通ページ
# =========================
class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


def loggedin_view(request):
    return render(request, 'loggedin_template.html', {
        'message': 'ログインしました。ようこそ！',
    })


# =========================
# Person
# =========================
@login_required
def person_list(request):
    persons = Person.objects.all()
    return render(request, 'myapp/person_list.html', {
        'persons': persons
    })


# =========================
# MyApp（CRUD）
# =========================
def myappListView(request):
    count = MyApp.objects.count()
    return HttpResponse(f"MyApp count = {count}")



def myappDetailView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)
    return render(request, "myapp/myapp_detail.html", {
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
@login_required
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
        search = search_form.cleaned_data.get('search')
        if search:
            objects = objects.filter(subject__icontains=search)

    return render(request, 'myapp/mymail_list.html', {
        'object_list': objects,
        'search_form': search_form,
    })

# =========================
# User Signup（一般ユーザー登録）
# =========================
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動ログイン
            return redirect("myapp:person_list")  # ログイン後ページ
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {
        "form": form
    })
