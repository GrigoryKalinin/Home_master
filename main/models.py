from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория') # название категории
    slug = models.SlugField(max_length=100, unique=True, verbose_name='url') # человекочитаемый URL
    image = models.ImageField(upload_to='images/category/', verbose_name='Изображение')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    description = models.TextField(max_length=100, blank=True, verbose_name='Описание')

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
        return reverse("main:product_by_category", args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория') # связь с категорией
    name = models.CharField(max_length=100, db_index=True, verbose_name='Продукт') # название товара
    slug = models.SlugField(max_length=100, unique=True, verbose_name='url') # человекочитаемый URL
    image = models.ImageField(upload_to='images/products/', blank=True, verbose_name='Изображение') # изображение товара
    description = models.TextField(blank=True, verbose_name='Описание') # описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена') # цена товара
    popularity = models.PositiveIntegerField(default=0, verbose_name='Популярность', blank=True) # популярность товара
    available = models.BooleanField(default=True, verbose_name='Доступность') # доступность товара
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # дата создания товара
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления') # дата обновления товара

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

        indexes = [
            models.Index(fields=['available', 'name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('canceled', 'Отменен'),
        ('in_work', 'В работе'),
        ('completed', 'Выполнен'),
        ('spam', 'Спам'),
    ]

    name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон', db_index=True)
    city = models.CharField(max_length=50, blank=True, verbose_name='Адрес')
    comment = models.TextField(max_length=100, blank=True, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    def __str__(self):
        return f'{self.name} ({self.phone})'

    class Meta: 
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

        indexes = [
            models.Index(fields=['status', 'phone', 'created']),
        ]