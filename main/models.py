from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# from django.core.validators import MinValueValidator, MaxValueValidator

# from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
from transliterate import translit


def create_slug(text):
    """Создает slug с поддержкой кириллицы"""
    try:
        # Транслитерация кириллицы в латиницу
        transliterated = translit(text, "ru", reversed=True)
        return slugify(transliterated)
    except:
        # Если транслитерация не удалась, используем стандартный slugify
        return slugify(text, allow_unicode=True)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")  # название категории
    slug = models.SlugField(max_length=100, unique=True, verbose_name="url")  # человекочитаемый URL
    image = models.ImageField(upload_to="images/category/", verbose_name="Изображение")
    available = models.BooleanField(default=True, verbose_name="Доступность")
    description = models.TextField(max_length=100, blank=True, verbose_name="Описание")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    popularity = models.PositiveIntegerField(default=0, verbose_name="Популярность", blank=True)  # популярность товара

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        # Генерируем slug если он пустой или имя изменилось
        if not self.slug or self._name_changed():
            self.slug = create_slug(self.name)

            # Проверяем уникальность slug
            original_slug = self.slug
            counter = 1
            while (
                self.__class__.objects.filter(slug=self.slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def _name_changed(self):
        """Проверяет, изменилось ли имя категории"""
        if not self.pk:  # Новый объект - считаем что имя "изменилось"
            return True

        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            return old_obj.name != self.name
        except self.__class__.DoesNotExist:
            return True

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("main:product_list", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,related_name="products",on_delete=models.CASCADE,verbose_name="Категория",)  # связь с категорией
    name = models.CharField(max_length=100, db_index=True, verbose_name="Продукт")  # название товара
    slug = models.SlugField(max_length=100, unique=True, verbose_name="url")  # человекочитаемый URL
    image = models.ImageField(upload_to="images/products/", blank=True, verbose_name="Изображение")  # изображение товара
    description = models.TextField(blank=True, verbose_name="Описание")  # описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")  # цена товара
    available = models.BooleanField(default=True, verbose_name="Доступность")  # доступность товара
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # дата создания товара
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # дата обновления товара
    popularity = models.PositiveIntegerField(default=0, verbose_name="Популярность", blank=True)  # популярность товара

    class Meta:
        ordering = ("name",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

        indexes = [
            models.Index(fields=["available", "name"]),
        ]

    def save(self, *args, **kwargs):
        # Генерируем slug если он пустой или имя изменилось
        if not self.slug or self._name_changed():
            self.slug = create_slug(self.name)

            # Проверяем уникальность slug
            original_slug = self.slug
            counter = 1
            while (
                self.__class__.objects.filter(slug=self.slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def _name_changed(self):
        """Проверяет, изменилось ли имя категории"""
        if not self.pk:  # Новый объект - считаем что имя "изменилось"
            return True

        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            return old_obj.name != self.name
        except self.__class__.DoesNotExist:
            return True

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.category.slug, self.slug])


class Service(models.Model):
    product = models.ForeignKey(Product, related_name="services", on_delete=models.CASCADE, verbose_name="Товар")  # связь с товаром
    name = models.CharField(max_length=100, db_index=True, verbose_name="Услуга")  # название услуги
    slug = models.SlugField(max_length=100, unique=True, verbose_name="url")  # человекочитаемый URL
    description = models.TextField(blank=True, verbose_name="Описание")  # описание услуги
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")  # цена услуги
    available = models.BooleanField(default=True, verbose_name="Доступность")  # доступность услуги
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # дата создания услуги
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # дата обновления услуги
    popularity = models.PositiveIntegerField(default=0, verbose_name="Популярность", blank=True)  # популярность

    class Meta:
        ordering = ("name",)
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

        indexes = [
            models.Index(fields=["available", "name"]),
        ]

    def save(self, *args, **kwargs):
        # Генерируем slug если он пустой или имя изменилось
        if not self.slug or self._name_changed():
            self.slug = create_slug(self.name)

            # Проверяем уникальность slug
            original_slug = self.slug
            counter = 1
            while (
                self.__class__.objects.filter(slug=self.slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def _name_changed(self):
        """Проверяет, изменилось ли имя категории"""
        if not self.pk:  # Новый объект - считаем что имя "изменилось"
            return True

        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            return old_obj.name != self.name
        except self.__class__.DoesNotExist:
            return True

    def __str__(self):
        return str(self.name)


class Employee(models.Model):
    STATUS_CHOICES = [
        ('trainee', 'Стажировка'),
        ('active', 'Основной состав'),
        ('vacation', 'В отпуске'),
        ('sick_leave', 'На больничном'),
        ('fired', 'Уволен'),
        ('remote', 'Удалённая работа'),
        ('part_time', 'Частичная занятость'),
        ('maternity', 'Декретный отпуск'),
        ('business_trip', 'В командировке'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", db_index=True)
    midle_name = models.CharField(max_length=50, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    email = models.EmailField(verbose_name="Email", blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", db_index=True)
    specialization = models.CharField(max_length=100, verbose_name="Специализация", db_index=True)
    experience = models.PositiveIntegerField(verbose_name="Опыт работы", help_text="В годах")
    image = models.ImageField(upload_to="images/employees/", blank=True, verbose_name="Фото")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    date_hired = models.DateField(verbose_name="Дата приема на работу", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="url", blank=True)
    available = models.BooleanField(default=True, verbose_name="Доступность")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        
    def save(self, *args, **kwargs):
        if not self.slug or self._name_changed():
            self.slug = create_slug(f"{self.first_name}-{self.last_name}")

            original_slug = self.slug
            counter = 1
            while (
                self.__class__.objects.filter(slug=self.slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def _name_changed(self):
        """Проверяет, изменилось ли имя категории"""
        if not self.pk:  # Новый объект - считаем что имя "изменилось"
            return True

        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            return (old_obj.first_name != self.first_name or 
                    old_obj.last_name != self.last_name)
        except self.__class__.DoesNotExist:
            return True

    def get_absolute_url(self):
        return reverse("main:employee_detail", args=[self.slug])

    def __str__(self):
        return f"{self.first_name} {self.last_name} специализация: {self.specialization} ({self.phone})"



class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("confirmed", "Подтвержден"),
        ("canceled", "Отменен"),
        ("in_work", "В работе"),
        ("completed", "Выполнен"),
        ("spam", "Спам"),
    ]

    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    image = models.ImageField(upload_to="images/orders/", blank=True, verbose_name="Фото")
    city = models.CharField(max_length=50, blank=True, verbose_name="Адрес")
    comment = models.TextField(max_length=100, blank=True, verbose_name="Комментарий")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

        indexes = [
            models.Index(fields=["status", "phone", "date_created"]),
        ]


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("invited", "Приглашен"),
        ("rejected", "Отклонен"),
        ("hired", "Нанят"),
        ("spam", "Спам"),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    phone = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    city = models.CharField(max_length=100, verbose_name="Город")
    specialization = models.CharField(max_length=100, verbose_name="Специализация", db_index=True)
    comment = models.TextField(max_length=1000, verbose_name="Комментарий", blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}, возвраст: {self.age}, город: {self.city}, специализация: {self.specialization}"

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

        indexes = [
            models.Index(fields=["city", "specialization"]),
        ]


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
#     name = models.CharField(max_length=100, verbose_name='Имя', blank=True)  # оставляем для совместимости
#     text = models.TextField(max_length=1000, verbose_name='Текст')
#     image = models.ImageField(upload_to='images/reviews/', blank=True, verbose_name='Фото')
#     date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     rating = models.PositiveIntegerField(default=5, verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

#     def get_name(self):
#         return self.user.get_full_name() or self.user.username if self.user else self.name

#     def save(self, *args, **kwargs):
#         if self.user and not self.name:
#             self.name = self.user.get_full_name() or self.user.username
#         super().save(*args, **kwargs)
