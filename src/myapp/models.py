from django.db import models
from django.conf import settings


class MyApp(models.Model):
    class Meta:
        # 本番DBにあるテーブル名に合わせる（dbcheckで myapp_diary が存在）
        db_table = "myapp_diary"

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="作成者",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")

    def __str__(self):
        # 一覧ではタイトルのみ表示
        return self.title


class Person(models.Model):
    class Meta:
        db_table = "person"

    name = models.CharField(verbose_name="名前", max_length=255)
    age = models.IntegerField(verbose_name="年齢")
    email = models.EmailField(verbose_name="メール", default="")
    phone = models.CharField(verbose_name="電話", max_length=20, default="")
    address = models.CharField(verbose_name="住所", max_length=255, default="")

    def __str__(self):
        return f"{self.name}({self.age}才)"


class MyMail(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
