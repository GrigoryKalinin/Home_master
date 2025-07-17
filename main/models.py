from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория') # название категории
    slug = models.SlugField(max_length=100, unique=True, verbose_name='url') # человекочитаемый URL 
    image = models.ImageField(upload_to='images/category/', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория') # связь с категорией
    name = models.CharField(max_length=100, db_index=True, verbose_name='Продукт') # название товара
    slug = models.SlugField(max_length=100, unique=True, verbose_name='url') # человекочитаемый URL
    image = models.ImageField(upload_to='images/products/', blank=True) # изображение товара
    description = models.TextField(blank=True, verbose_name='Описание') # описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена') # цена товара
    available = models.BooleanField(default=True, verbose_name='Доступность') # доступность товара
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # дата создания товара
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления') # дата обновления товара

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])