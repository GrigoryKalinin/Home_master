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


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Специализация")
    categories = models.ManyToManyField('Category', blank=True, verbose_name="Категории")
    
    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        ordering = ['name']
    
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
    middle_name = models.CharField(max_length=50, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    email = models.EmailField(verbose_name="Email", blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", db_index=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="Специализация")
    categories = models.ManyToManyField('Category', blank=True, verbose_name="Категории работ")
    products = models.ManyToManyField('Product', blank=True, verbose_name="Товары")
    services = models.ManyToManyField('Service', blank=True, verbose_name="Услуги")
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
        indexes = [
            models.Index(fields=['status', 'available']),
            models.Index(fields=['specialization', 'city']),
        ]
        
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

    def get_experience_display(self):
        """Возвращает опыт работы с правильным склонением"""
        exp = self.experience
        last_digit = exp % 10
        last_two_digits = exp % 100
        
        if last_two_digits >= 11 and last_two_digits <= 14:
            return f"{exp} лет"
        
        if last_digit == 1:
            return f"{exp} год"
        elif last_digit >= 2 and last_digit <= 4:
            return f"{exp} года"
        else:
            return f"{exp} лет"

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
        ("failed", "Не удалось связаться"),
        ("callback", "Перезвонить"),
    ]

    # Основная информация из заявки
    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    image = models.ImageField(upload_to="images/orders/", blank=True, verbose_name="Фото")
    city = models.CharField(max_length=50, blank=True, verbose_name="Адрес")
    comment = models.TextField(max_length=100, blank=True, verbose_name="Комментарий")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    created_by_client = models.BooleanField(default=False, verbose_name="Создано клиентом")
    
    # Дополнительная информация (заполняется при редактировании)
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия клиента")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество клиента")
    address = models.CharField(max_length=200, blank=True, verbose_name="Полный адрес")
    work_description = models.TextField(blank=True, verbose_name="Описание работ")
    categories = models.ManyToManyField('Category', blank=True, verbose_name="Категории")
    products = models.ManyToManyField('Product', blank=True, verbose_name="Товары")
    assigned_employees = models.ManyToManyField('Employee', blank=True, verbose_name="Назначенные мастера")

    def get_display_name(self):
        """Возвращает полное имя если есть, иначе обычное имя"""
        if self.last_name:
            full_name = f"{self.last_name} {self.name}"
            if self.middle_name:
                full_name += f" {self.middle_name}"
            return full_name
        return self.name
    
    def get_display_address(self):
        """Возвращает полный адрес если есть, иначе город"""
        return self.address if self.address else self.city

    def __str__(self):
        return f"{self.get_display_name()} ({self.phone})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

        indexes = [
            models.Index(fields=["status", "phone", "date_created"]),
        ]


class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='additional_images_set', verbose_name="Заказ")
    image = models.ImageField(upload_to="images/orders/additional/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Дополнительное изображение заказа"
        verbose_name_plural = "Дополнительные изображения заказов"
    
    def __str__(self):
        return f"Изображение для заказа #{self.order.id}"


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
    created_by_client = models.BooleanField(default=False, verbose_name="Создано клиентом")

    def get_age_display(self):
        """Возвращает возраст с правильным склонением"""
        age = self.age
        last_digit = age % 10
        last_two_digits = age % 100
        
        if last_two_digits >= 11 and last_two_digits <= 14:
            return f"{age} лет"
        
        if last_digit == 1:
            return f"{age} год"
        elif last_digit >= 2 and last_digit <= 4:
            return f"{age} года"
        else:
            return f"{age} лет"

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
