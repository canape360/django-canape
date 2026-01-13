from django.contrib import admin
from .models import MyApp, Person, MyMail

# MyApp 用の admin クラス
class MyAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')  # timestamp → created_at に変更し、作成者も表示

# モデルを admin に登録
admin.site.register(MyApp, MyAppAdmin)
admin.site.register(Person)
admin.site.register(MyMail)
