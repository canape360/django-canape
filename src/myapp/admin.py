from django.contrib import admin
from .models import MyApp, Person, MyMail


# MyApp 用の admin クラス
class MyAppAdmin(admin.ModelAdmin):
    # author → user に修正
    list_display = ("title", "created_at", "user")


# モデルを admin に登録
admin.site.register(MyApp, MyAppAdmin)
admin.site.register(Person)
admin.site.register(MyMail)
