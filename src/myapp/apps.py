from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from django.conf import settings
        from django.contrib.auth import get_user_model
        import os

        # 本番（Render）だけで動かす
        if settings.DEBUG:
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        # 環境変数が揃っていなければ何もしない
        if not username or not password:
            return

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            # 🔑 既存ユーザーでも必ずパスワードを同期
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except User.DoesNotExist:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
