# diaryapp/models.py
from django.db import models
from django.conf import settings


class Diary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diaries",
        verbose_name="ユーザー",
    )

    title = models.CharField("タイトル", max_length=100)
    content = models.TextField("内容", blank=True)

    # 公開 / 非公開
    is_public = models.BooleanField("公開", default=False)

    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "日記"
        verbose_name_plural = "日記"

    def __str__(self):
        return self.title
