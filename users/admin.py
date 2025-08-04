from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = ('email', 'get_full_name', 'phone', 'city', 'is_active', 'is_staff', 'date_joined', 'marketing_consent1')
    list_filter = (
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'marketing_consent1',
        ('date_joined', RangeDateFilter)
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('last_login', 'date_joined')
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'last_name'
    
    fieldsets = (
        ('Аутентификация', {
            'fields': ('email', 'password')
        }),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'phone', 'city', 'address', 'avatar')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Согласия', {
            'fields': ('marketing_consent1', 'marketing_consent2')
        }),
        ('Системная информация', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Создание пользователя', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
