from django.contrib import admin
from .models import Category, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'available', 'slug'] # поля, которые будут отображаться в админке
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['name']
    list_editable = ['available'] # поля, которые можно редактировать

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =  ['name', 'category', 'price', 'available','popularity', 'date_created', 'date_updated', 'slug'] # поля, которые будут отображаться в админке
    list_filter = ['available', 'date_created', 'date_updated', 'category'] # поля, по которым будет фильтрация
    list_editable = ['price', 'available', 'popularity'] # поля, которые можно редактировать
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['category__name', 'name',]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'comment', 'date_created', 'status', 'date_updated']
    list_filter = ['status', 'date_created']
    list_editable = ['status']
    search_fields = ['name', 'phone']
