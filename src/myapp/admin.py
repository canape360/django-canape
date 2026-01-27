from django.contrib import admin
from .models import MyApp, Person, MyMail


class MyAppAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "user")


admin.site.register(MyApp, MyAppAdmin)
admin.site.register(Person)
admin.site.register(MyMail)
