from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', db_index=True)
    last_name = models.CharField(max_length=150,verbose_name='Фамилия', db_index=True)
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, db_index=True, region="RU")
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')
    

    # Настройки аутентификации
    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Обязательные поля при createsuperuser

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