from django.db import models
from django.conf import settings


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


class MyApp(models.Model):
    class Meta:
        db_table = "myapp_diary"

    # DB: title (varchar, NOT NULL)
    title = models.CharField(max_length=100)

    # DB: body (text, NOT NULL)
    body = models.TextField(db_column="body")

    # DB: created_at (timestamptz, NOT NULL)
    # 既存DBの値を使うので auto_now_add は付けない
    created_at = models.DateTimeField(db_column="created_at", verbose_name="作成日")

    # DB: user_id (integer, NULL)
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
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="person_id",
        related_name="myapp_diaries",
        verbose_name="人物",
    )

    def __str__(self):
        return self.title


class MyMail(models.Model):
    class Meta:
        db_table = "myapp_mymail"  # もし dbcheck で違うなら合わせてください

    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
