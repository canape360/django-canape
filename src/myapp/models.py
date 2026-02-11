from django.db import models
from django.conf import settings
from django.utils import timezone


class Person(models.Model):
    class Meta:
        db_table = "person"
        managed = False

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.name}({self.age}才)"


class MyApp(models.Model):
    class Meta:
        # ✅ Supabaseに実在するテーブル名に合わせる（重要）
        # あなたのSupabase一覧に myapp_myapp があったのでこちらが正解のはず
        db_table = "myapp_myapp"
        managed = False

    title = models.CharField(max_length=100)
    body = models.TextField(db_column="body")

    # ✅ DBが NOT NULL でも落ちないようにデフォルトを付与
    # 既存行にNULLがあり得るDBなら、null=Trueにする（ただしDB制約がNOT NULLなら意味なし）
    created_at = models.DateTimeField(db_column="created_at", default=timezone.now)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="user_id",
        related_name="myapp_diaries",
    )

    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="person_id",
        related_name="myapp_diaries",
    )

    def __str__(self):
        return self.title


class MyMail(models.Model):
    class Meta:
        db_table = "myapp_mymail"
        managed = False

    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
