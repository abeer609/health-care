from django.contrib import admin
from .models import User
from unfold.admin import ModelAdmin as UnfoldModelAdmin


@admin.register(User)
class UserAdmin(UnfoldModelAdmin):
    search_fields = ["email", "username"]
