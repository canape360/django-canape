import os
from django.db import models
from django.conf import settings
from django.utils import timezone

# 本番(Render/Supabase)では USE_SUPABASE=1 を設定
USE_SUPABASE = os.getenv("USE_SUPABASE", "").lower() in ("1", "true", "yes")


class Person(models.Model):
    """
    Supabase/SQLite: person テーブル
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
    ローカル(SQLite): myapp_myapp(title, body, created_at, person_id, user_id)
    Supabase(Postgres): myapp_myapp(title, content, created_at, author_id)
    """
    class Meta:
        db_table = "myapp_myapp"
        managed = False

    title = models.CharField(max_length=100)

    # 本文: Supabaseは content / ローカルは body
    body = models.TextField(db_column="content" if USE_SUPABASE else "body")

    created_at = models.DateTimeField(db_column="created_at", default=timezone.now)

    # ユーザー: Supabaseは author_id / ローカルは user_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="author_id" if USE_SUPABASE else "user_id",
        related_name="myapp_entries",
    )

    # person_id はローカルSQLiteにある（Supabaseに無い想定なら、Supabaseでは使わない）
    if not USE_SUPABASE:
        person_id = models.BigIntegerField(db_column="person_id", null=True, blank=True)

    def __str__(self):
        return self.title


class MyMail(models.Model):
    """
    Supabase/SQLite: myapp_mymail テーブル
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