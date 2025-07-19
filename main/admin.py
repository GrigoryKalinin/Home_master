from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'available', 'slug'] # поля, которые будут отображаться в админке
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['name']
    list_editable = ['available'] # поля, которые можно редактировать

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =  ['name', 'category', 'price', 'available','popularity', 'date_created', 'date_update', 'slug'] # поля, которые будут отображаться в админке
    list_filter = ['available', 'date_created', 'date_update', 'category'] # поля, по которым будет фильтрация
    list_editable = ['price', 'available', 'popularity'] # поля, которые можно редактировать
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['category__name', 'name',]
