# diaryapp/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Diary
from .forms import DiaryForm


# =========================
# 自分用（ログイン必須）
# =========================
class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = "diaryapp/diary_list.html"
    context_object_name = "diaries"

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user).order_by("-created_at")


class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = Diary
    template_name = "diaryapp/diary_detail.html"

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = "diaryapp/diary_form.html"
    success_url = reverse_lazy("diaryapp:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = "diaryapp/diary_form.html"
    success_url = reverse_lazy("diaryapp:list")

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Diary
    template_name = "diaryapp/diary_confirm_delete.html"
    success_url = reverse_lazy("diaryapp:list")

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


# =========================
# 公開（ログイン不要）
# =========================
class PublicDiaryListView(ListView):
    model = Diary
    template_name = "diaryapp/public_diary_list.html"
    context_object_name = "diaries"
    paginate_by = 20  # 任意

    def get_queryset(self):
        return Diary.objects.filter(is_public=True).select_related("user").order_by("-created_at")


class PublicDiaryDetailView(DetailView):
    model = Diary
    template_name = "diaryapp/public_diary_detail.html"

    def get_queryset(self):
        # 非公開は 404
        return Diary.objects.filter(is_public=True).select_related("user")
