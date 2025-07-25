from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order


class OrderForm(forms.ModelForm):

    phone = PhoneNumberField(
        region='RU',
        label='Ваш телефон',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control phone-mask',
            'data-mask': '+7 (000) 000-00-00',
            'inputmode': 'tel'  # Оптимизация для мобильных устройств
        }),
        error_messages={
            'invalid': 'Введите корректный номер телефона',
            'required': 'Телефон обязателен для заполнения'
        }
    )

    name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя',
            'autocomplete': 'name'  # Для автозаполнения
        })
    )

    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите комментарий (необязательно)',
            'rows': 2,
        })
    )

    class Meta:
        model = Order
        fields = [ 'phone', 'name', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем стандартный российский регион для всех номеров
        self.fields['phone'].initial = '+7'


# class ReviewForm(forms.ModelForm):
#     RATING_CHOICES = [
#         (1, '1 - Ужасно'),
#         (2, '2 - Плохо'), 
#         (3, '3 - Нормально'),
#         (4, '4 - Хорошо'),
#         (5, '5 - Отлично'),
#     ]

#     class Meta:
#         model = Review
#         fields = ['text', 'image', 'rating']