from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True) # название категории
    slug = models.SlugField(max_length=100, unique=True) # человекочитаемый URL 

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # связь с категорией
    name = models.CharField(max_length=100, db_index=True) # название товара
    slug = models.SlugField(max_length=100, unique=True) # человекочитаемый URL
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) # изображение товара
    description = models.TextField(blank=True) # описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2) # цена товара
    available = models.BooleanField(default=True) # доступность товара
    date_created = models.DateTimeField(auto_now_add=True) # дата создания товара
    date_update = models.DateTimeField(auto_now=True) # дата обновления товара

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.name)