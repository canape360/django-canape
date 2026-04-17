from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone  # ★追加（created_at用）

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
    # 大量データでも重くなりにくいように上限（必要なら数値変更）
    objects = MyApp.objects.all().order_by("-id")[:500]
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

            # ★重要：DBがNOT NULLでも落ちないように必ず埋める
            if not getattr(obj, "created_at", None):
                obj.created_at = timezone.now()

            obj.save()
            messages.success(request, "日記を保存しました")
            return redirect("myapp:detail", pk=obj.pk)

        return render(request, "myapp/myapp_form.html", {"form": form})

    form = MyAppForm()
    return render(request, "myapp/myapp_form.html", {"form": form})


@login_required
def myappUpdateView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)

    # （任意）自分の投稿だけ編集可能にしたい場合はコメント解除
    # if obj.user_id and obj.user_id != request.user.id:
    #     messages.error(request, "この日記を編集する権限がありません")
    #     return redirect("myapp:detail", pk=obj.pk)

    if request.method == "POST":
        form = MyAppForm(request.POST, instance=obj)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.user = request.user

            # ★重要：古いNULLデータを編集しても落ちない
            if not getattr(updated, "created_at", None):
                updated.created_at = timezone.now()

            updated.save()
            messages.success(request, "日記を更新しました")
            return redirect("myapp:detail", pk=updated.pk)

        return render(request, "myapp/myapp_update.html", {"form": form, "object": obj})

    form = MyAppForm(instance=obj)
    return render(request, "myapp/myapp_update.html", {"form": form, "object": obj})


@login_required
def myappDeleteView(request, pk):
    obj = get_object_or_404(MyApp, pk=pk)

    # （任意）自分の投稿だけ削除可能にしたい場合はコメント解除
    # if obj.user_id and obj.user_id != request.user.id:
    #     messages.error(request, "この日記を削除する権限がありません")
    #     return redirect("myapp:detail", pk=obj.pk)

    if request.method == "POST":
        obj.delete()
        messages.success(request, "日記を削除しました")
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

        return render(request, "myapp/mymail-form.html", {"form": form})

    form = MyMailForm()
    return render(request, "myapp/mymail-form.html", {"form": form})


@login_required
def mymail_list(request):
    search_form = MyMailSearchForm(request.GET)
    objects = MyMail.objects.all().order_by("-id")[:500]

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
            messages.success(request, "登録が完了しました")
            return redirect("myapp:person_list")

        return render(request, "registration/signup.html", {"form": form})

    form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def top(request):
    context = {
        "title": "ようこそ",
        "message": "これは一般ユーザー向けの画面です。",
    }
    return render(request, "myapp/top.html", context)
