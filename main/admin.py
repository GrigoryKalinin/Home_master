from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, Service, Order, JobApplication, Employee

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'available', 'popularity', 'slug', 'date_created', 'date_updated'] # поля, которые будут отображаться в админке
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['name']
    list_editable = ['available', 'popularity'] # поля, которые можно редактировать
    list_filter = ['available', 'popularity', 'date_created', 'date_updated',]

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display =  ['name', 'category', 'price', 'available', 'popularity', 'slug', 'date_updated'] # поля, которые будут отображаться в админке
    list_filter = ['available', 'category', 'popularity', 'date_updated'] # поля, по которым будет фильтрация
    list_editable = ['price', 'available', 'popularity'] # поля, которые можно редактировать
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['category__name', 'name']

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'product', 'product__category__name' ,'price', 'available', 'slug', 'popularity', 'date_updated'] # поля, которые будут отображаться в админке
    list_filter = ['available', 'product', 'popularity', 'date_updated', 'product__category__name'] # поля, по которым будет фильтрация
    list_editable = ['price', 'available', 'popularity'] # поля, которые можно редактировать
    prepopulated_fields = {'slug': ('name',)} # автоматическое заполнение поля slug по полю name
    search_fields = ['product__name', 'name', 'product__category__name'] # поля, по которым будет поиск 

@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'specialization', 'status', 'available', 'experience','date_hired']
    list_filter = ['status', 'date_hired', 'city', 'specialization']
    list_editable = ['status', 'experience', 'available']
    search_fields = ['first_name', 'last_name', 'phone', 'specialization', 'status']

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['name', 'status', 'phone', 'comment', 'date_created']
    list_filter = ['status', 'date_created']
    list_editable = ['status']
    search_fields = ['name', 'phone']

@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'status', 'age', 'phone', 'city', 'specialization', 'date_created',]
    list_filter = ['status', 'date_created', 'city', 'specialization']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'phone', 'city', 'specialization',]