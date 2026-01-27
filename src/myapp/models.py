from django.db import models
from django.conf import settings


class MyApp(models.Model):
    class Meta:
        db_table = "myapp_diary"

    title = models.CharField(max_length=100)

    # DB: body (text, NOT NULL)
    body = models.TextField(db_column="body")

    # DB: created_at (timestamptz, NOT NULL)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="created_at",
        verbose_name="作成日",
    )

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
