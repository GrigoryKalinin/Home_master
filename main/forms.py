from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.formfields import PhoneNumberField
from .models import Order, JobApplication, Employee, Category, Product, Service, Specialization

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image", "available"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['product', 'name', 'description', 'price', 'available']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EmployeeForm(forms.ModelForm):

    first_name = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваше имя",
                "class": "form-control",
                "autocomplete": "given-name",  # Для автозаполнения
            }
        ),
    )

    last_name = forms.CharField(
        label="Ваша фамилия",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите вашу фамилию",
                "class": "form-control",
                "autocomplete": "family-name",  # Для автозаполнения
            }
        ),
    )

    midle_name = forms.CharField(
        label="Ваше отчество",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваше отчество",
                "class": "form-control",
                "autocomplete": "additional-name",  # Для автозаполнения
            }
        ),
    )

    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(
            attrs={
                "placeholder": "Введите дату рождения",
                "type": "date",
                "class": "form-control",
                "autocomplete": "off",
            },
            format='%Y-%m-%d'  # Добавляем формат
        ),
        input_formats=['%Y-%m-%d']  # Добавляем входной формат
    )

    phone = PhoneNumberField(
        region="RU",
        label="Ваш телефон",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7 (999) 123-45-67",
                "class": "form-control phone-mask",
                "data-mask": "+7 (000) 000-00-00",
                "autocomplete": "off",  # Для автозаполнения
                "inputmode": "tel",  # Оптимизация для мобильных устройств
            }
        ),
        error_messages={
            "invalid": "Введите корректный номер телефона",
            "required": "Телефон обязателен для заполнения",
        },
    )

    email = forms.EmailField(
        label="Ваш email",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Введите ваш email",
                "class": "form-control",
                "autocomplete": "email",  # Для автозаполнения
            }
        ),
    )

    city = forms.CharField(
        label="Ваш город",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваш город",
                "class": "form-control",
                "autocomplete": "address-level2",  # Для автозаполнения
            }
        ),
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        label="Специализация",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    experience = forms.IntegerField(
        label="Опыт работы",
        help_text="В годах (целое число от 0 до 70)",
        widget=forms.NumberInput(
            attrs={
                "min": 0,
                "max": 70,
                "step": 1,
                "autocomplete": "off",
                "class": "form-control",
            }
        ),
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )

    date_hired = forms.DateField(
        label="Дата приема на работу",
        widget=forms.DateInput(
            attrs={
                "type": "date", 
                "class": "form-control"
            },
            format='%Y-%m-%d'  # Добавляем формат
        ),
        input_formats=['%Y-%m-%d']  # Добавляем входной формат
    )

    status = forms.ChoiceField(
        label="Статус",
        choices=[
            ("trainee", "Стажировка"),
            ("active", "Основной состав"),
            ("remote", "Удалённая работа"),
            ("part_time", "Частичная занятость"),
        ],
        initial="active",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    image = forms.ImageField(
        label="Фотография",
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control-file", "accept": "image/*"}
        ),
    )

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "midle_name",
            "birth_date",
            "phone",
            "email",
            "city",
            "specialization",
            "experience",
            "date_hired",
            "status",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем стандартный российский регион для всех номеров
        self.fields["phone"].initial = "+7"


class OrderForm(forms.ModelForm):

    phone = PhoneNumberField(
        region="RU",
        label="Ваш телефон",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7 (999) 123-45-67",
                "class": "form-control phone-mask",
                "data-mask": "+7 (000) 000-00-00",
                "autocomplete": "tel",  # Для автозаполнения
                "inputmode": "tel",  # Оптимизация для мобильных устройств
            }
        ),
        error_messages={
            "invalid": "Введите корректный номер телефона",
            "required": "Телефон обязателен для заполнения",
        },
    )

    name = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваше имя",
                "class": "form-control",
                "autocomplete": "name",  # Для автозаполнения
            }
        ),
    )

    comment = forms.CharField(
        required=False,
        label="Комментарий",
        help_text="Необязательно",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Введите комментарий (необязательно)",
                "rows": 2,
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Order
        fields = ["phone", "name", "comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем стандартный российский регион для всех номеров
        self.fields["phone"].initial = "+7"


class JobApplicationForm(forms.ModelForm):

    first_name = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваше имя",
                "class": "form-control",
                "autocomplete": "given-name",  # Для автозаполнения
            }
        ),
    )

    last_name = forms.CharField(
        label="Ваша фамилия",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите вашу фамилию",
                "class": "form-control",
                "autocomplete": "family-name",  # Для автозаполнения
            }
        ),
    )

    age = forms.IntegerField(
        label="Ваш возраст",
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Введите ваш возраст",
                "class": "form-control",
            }
        ),
    )

    phone = PhoneNumberField(
        region="RU",
        label="Ваш телефон",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7 (999) 123-45-67",
                "class": "form-control phone-mask",
                "data-mask": "+7 (000) 000-00-00",
                "autocomplete": "tel",  # Для автозаполнения
                "inputmode": "tel",  # Оптимизация для мобильных устройств
            }
        ),
        error_messages={
            "invalid": "Введите корректный номер телефона",
            "required": "Телефон обязателен для заполнения",
        },
    )

    city = forms.CharField(
        label="Ваш город",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ваш город",
                "class": "form-control",
                "autocomplete": "address-level2",  # Для автозаполнения
            }
        ),
    )

    specialization = forms.CharField(
        label="Ваша специализация",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите вашу специализацию",
                "class": "form-control",
            }
        ),
    )

    comment = forms.CharField(
        label="Дполнительная информация",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Введите дополнительную информацию (необязательно)",
                "rows": 2,
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = JobApplication
        fields = ["first_name", "last_name", "age", "phone", "city", "specialization"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем стандартный российский регион для всех номеров
        self.fields["phone"].initial = "+7"

class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название специализации'})
        }



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
