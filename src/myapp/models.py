from django.db import models
from django.conf import settings


class MyApp(models.Model):
    class Meta:
        db_table = "myapp_diary"

    # DB: title (varchar, NOT NULL)
    title = models.CharField(max_length=100)

    # DB: body (text, NOT NULL)  ※content ではない
    body = models.TextField()

    # DB: created_at (timestamptz, NOT NULL)
    # 既存DB列を読むだけ。auto_now_add は付けない
    created_at = models.DateTimeField()

    # DB: user_id (integer, NULL)
    # 既存の user_id 列にFKで紐づける
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="user_id",
        related_name="myapp_diaries",
        verbose_name="作成者",
    )

    # DB: person_id (bigint, NULL)
    # 既存の person_id 列にFKで紐づける（循環import回避のため文字列参照）
    person = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="person_id",
        related_name="myapp_diaries",
        verbose_name="人物",
    )

    def __str__(self):
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
