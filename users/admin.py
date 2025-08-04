from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_active', 'is_staff', 'date_joined', 'marketing_consent1')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'marketing_consent1', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'phone', 'city', 'address', 'avatar')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Согласия', {'fields': ('marketing_consent1', 'marketing_consent2')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )