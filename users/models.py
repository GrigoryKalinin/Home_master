from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Введите свой email')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Супер юзер должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Супер юзер должен иметь is_superuser=True.')
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', db_index=True)
    last_name = models.CharField(max_length=150,verbose_name='Фамилия', db_index=True)
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, db_index=True, region="RU")
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    address = models.CharField(max_length=200, blank=True, verbose_name='Адрес')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')
    marketing_consent1 = models.BooleanField(default=False, verbose_name='Согласие на рассылку')
    marketing_consent2 = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')
    username = None

    objects = CustomUserManager()

    # Настройки аутентификации
    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Обязательные поля при createsuperuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'.strip()

    def get_short_name(self):
        return self.first_name
    