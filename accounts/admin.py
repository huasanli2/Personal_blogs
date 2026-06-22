from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'nickname', 'email', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('nickname', 'avatar', 'bio')}),
    )
