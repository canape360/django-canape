from django.db import models
from django.conf import settings
from django.utils import timezone


class Person(models.Model):
    """
    Supabase: person テーブル
    """
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
    """
    Supabase: myapp_myapp テーブル
    columns:
      - id (bigint)
      - title (varchar)
      - content (varchar)  ← 本文
      - author_id (int)    ← ユーザー
      - created_at (timestamptz)
    """
    class Meta:
        db_table = "myapp_myapp"
        managed = False

    title = models.CharField(max_length=100)

    # ✅ DB列は content(varchar) なので db_column="content"
    # 文字数制限があるはずなので CharField が安全
    # ※必要なら max_length を増やしてください（DB側の制限に合わせる）
    body = models.CharField(db_column="content", max_length=2000)

    created_at = models.DateTimeField(db_column="created_at", default=timezone.now)

    # ✅ DB列は author_id（user_id ではない）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="author_id",
        related_name="myapp_entries",
    )

    # ❌ myapp_myapp には person_id 列が無いので person FK は持たない
    # person = models.ForeignKey(...)

    def __str__(self):
        return self.title


class MyMail(models.Model):
    """
    Supabase: myapp_mymail テーブル（あなたのDBに存在）
    """
    class Meta:
        db_table = "myapp_mymail"
        managed = False

    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
