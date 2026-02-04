from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from .models import MyApp, Person, MyMail
from .forms import MyAppForm, MyMailForm, MyMailSearchForm


@login_required
def user_dashboard(request):
    return render(request, "myapp/user_dashboard.html")


class AboutView(TemplateView):
    template_name = "about.html"
# =========================
# Person
# =========================
@login_required
def person_list(request):
    persons = Person.objects.all()
    return render(request, "myapp/person_list.html", {"persons": persons})


@login_required
def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, "myapp/person_detail.html", {"person": person})

# =========================
# MyApp（CRUD）
# =========================
@login_required
def myappListView(request):
    objects = MyApp.objects.all().order_by("-id")
    return render(request, "myapp/myapp_list.html", {"object_list": objects})


@login_required
def myapp_detail_latest(request):
    obj = MyApp.objects.order_by("-id").first()
    if not obj:
        return redirect("myapp:list")
    return redirect("myapp:detail", pk=obj.pk)


@login_required
def myappDetailView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)
    return render(request, "myapp/myapp_detail.html", {"object": obj})


@login_required
def myappCreateView(request):
    if request.method == "POST":
        form = MyAppForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # ✅ user に統一
            obj.save()
            return redirect("myapp:detail", pk=obj.pk)

        # ✅ バリデーションエラーがある場合は、そのままエラー付きで返す
        return render(request, "myapp/myapp_form.html", {"form": form})

    # GET
    form = MyAppForm()
    return render(request, "myapp/myapp_form.html", {"form": form})


@login_required
def myappUpdateView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)

    if request.method == "POST":
        form = MyAppForm(request.POST, instance=obj)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.user = request.user  # ✅ user に統一
            updated.save()
            return redirect("myapp:detail", pk=updated.pk)

        # ✅ エラー付きで返す
        return render(request, "myapp/myapp_update.html", {"form": form, "object": obj})

    # GET
    form = MyAppForm(instance=obj)
    return render(request, "myapp/myapp_update.html", {"form": form, "object": obj})


@login_required
def myappDeleteView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("myapp:list")
    return render(request, "myapp/delete_template.html", {"object": obj})


# =========================
# MyMail
# =========================
@login_required
def mymailCreateView(request):
    if request.method == "POST":
        form = MyMailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "メールを送信しました")
            return redirect("myapp:mymail_list")

        # ✅ エラー付きで返す
        return render(request, "myapp/mymail-form.html", {"form": form})

    form = MyMailForm()
    return render(request, "myapp/mymail-form.html", {"form": form})


@login_required
def mymail_list(request):
    search_form = MyMailSearchForm(request.GET)
    objects = MyMail.objects.all().order_by("-id")

    if search_form.is_valid():
        search = search_form.cleaned_data.get("search")
        if search:
            objects = objects.filter(subject__icontains=search)

    return render(
        request,
        "myapp/mymail_list.html",
        {"object_list": objects, "search_form": search_form},
    )


# =========================
# Signup
# =========================
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("myapp:person_list")
        # ✅ エラー付きで返す
        return render(request, "registration/signup.html", {"form": form})

    form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})



def top(request):
    context = {
        "title": "ようこそ",
        "message": "これは一般ユーザー向けの画面です。",
    }
    return render(request, "myapp/top.html", context)
