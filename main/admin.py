from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from .models import Category, Product, Service, Order, JobApplication, Employee, Specialization

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'available', 'popularity', 'slug', 'date_created', 'date_updated']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_editable = ['available', 'popularity']
    list_filter = [
        'available', 
        'popularity', 
        ('date_created', RangeDateFilter),
        ('date_updated', RangeDateFilter)
    ]
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Специализации', {
            'fields': ('specializations',)
        }),
        ('Настройки', {
            'fields': ('available', 'popularity')
        }),
        ('Системная информация', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'popularity', 'slug', 'date_updated']
    list_filter = [
        'available', 
        'category', 
        'popularity', 
        ('date_updated', RangeDateFilter)
    ]
    list_editable = ['price', 'available', 'popularity']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['category__name', 'name']
    list_select_related = ['category']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Цена и настройки', {
            'fields': ('price', 'available', 'popularity')
        }),
        ('Системная информация', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'product', 'get_category', 'price', 'available', 'popularity', 'date_updated']
    list_filter = [
        'available', 
        'product', 
        'popularity', 
        ('date_updated', RangeDateFilter),
        'product__category'
    ]
    list_editable = ['price', 'available', 'popularity']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['product__name', 'name', 'product__category__name']
    list_select_related = ['product', 'product__category']
    readonly_fields = ['date_created', 'date_updated']
    
    def get_category(self, obj):
        return obj.product.category.name
    get_category.short_description = 'Категория'
    get_category.admin_order_field = 'product__category__name'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'product', 'description')
        }),
        ('Цена и настройки', {
            'fields': ('price', 'available', 'popularity')
        }),
        ('Системная информация', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ['get_full_name', 'phone', 'city', 'specialization', 'status', 'available', 'experience', 'date_hired']
    list_filter = ['status', 'city', 'specialization', ('date_hired', RangeDateFilter)]
    list_editable = ['status', 'experience', 'available']
    search_fields = ['first_name', 'last_name', 'phone', 'specialization']
    readonly_fields = ['date_created', 'date_updated', 'slug']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'last_name'
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'midle_name', 'birth_date', 'image')
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'city')
        }),
        ('Работа', {
            'fields': ('specialization', 'products', 'services', 'experience', 'date_hired', 'status', 'available')
        }),
        ('Системная информация', {
            'fields': ('slug', 'date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'status', 'created_by_client', 'date_created']
    list_filter = ['status', 'created_by_client', ('date_created', RangeDateFilter)]
    list_editable = ['status']
    search_fields = ['name', 'phone']
    readonly_fields = ['date_created']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('name', 'phone', 'city', 'comment', 'image')
        }),
        ('Статус', {
            'fields': ('status', 'created_by_client')
        }),
        ('Системная информация', {
            'fields': ('date_created',),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ['get_full_name', 'age', 'phone', 'city', 'specialization', 'status', 'date_created']
    list_filter = ['status', 'city', 'specialization', ('date_created', RangeDateFilter)]
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'phone', 'city', 'specialization']
    readonly_fields = ['date_created']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'last_name'
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'age', 'phone', 'city')
        }),
        ('Профессиональная информация', {
            'fields': ('specialization', 'comment')
        }),
        ('Статус', {
            'fields': ('status', 'created_by_client')
        }),
        ('Системная информация', {
            'fields': ('date_created',),
            'classes': ('collapse',)
        }),
    )
