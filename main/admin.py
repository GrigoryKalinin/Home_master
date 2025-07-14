from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug'] # поля, которые будут отображаться в админке
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =  ['name', 'category', 'price', 'available', 'date_created', 'date_update'] # поля, которые будут отображаться в админке
    list_filter = ['available', 'date_created', 'date_update', 'category'] # поля, по которым будет фильтрация
    list_editable = ['price', 'available'] # поля, которые можно редактировать
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name