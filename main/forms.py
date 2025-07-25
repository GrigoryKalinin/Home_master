from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order, JobApplication


class OrderForm(forms.ModelForm):

    phone = PhoneNumberField(
        region='RU',
        label='Ваш телефон',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control phone-mask',
            'data-mask': '+7 (000) 000-00-00',
            'autocomplete': 'tel',  # Для автозаполнения
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
            'class': 'form-control',
            'autocomplete': 'name'  # Для автозаполнения
        })
    )

    comment = forms.CharField(
        required=False,
        label='Комментарий',
        help_text='Необязательно',
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите комментарий (необязательно)',
            'rows': 2,
            'class': 'form-control'
        })
    )

    class Meta:
        model = Order
        fields = [ 'phone', 'name', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем стандартный российский регион для всех номеров
        self.fields['phone'].initial = '+7'


class JobApplicationForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя',
            'class': 'form-control',
            'autocomplete': 'given-name'  # Для автозаполнения
        })
    )

    last_name = forms.CharField(
        label='Ваша фамилия',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите вашу фамилию',
            'class': 'form-control',
            'autocomplete': 'family-name'  # Для автозаполнения
        })
    )

    age = forms.IntegerField(
        label='Ваш возраст',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите ваш возраст',
            'class': 'form-control',
        })
    )

    phone = PhoneNumberField(
        region='RU',
        label='Ваш телефон',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control phone-mask',
            'data-mask': '+7 (000) 000-00-00',
            'autocomplete': 'tel',  # Для автозаполнения
            'inputmode': 'tel'  # Оптимизация для мобильных устройств
        }),
        error_messages={
            'invalid': 'Введите корректный номер телефона',
            'required': 'Телефон обязателен для заполнения'
        }
    )

    city = forms.CharField(
        label='Ваш город',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваш город',
            'class': 'form-control',
            'autocomplete': 'address-level2'  # Для автозаполнения
        })
    )

    specialization = forms.CharField(
        label='Ваша специализация',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите вашу специализацию',
            'class': 'form-control',
        })
    )

    comment = forms.CharField(
        label='Дполнительная информация',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите дополнительную информацию (необязательно)',
            'rows': 2,
            'class': 'form-control'
        })
    )

    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'age', 'phone', 'city', 'specialization']

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