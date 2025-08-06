from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.formfields import PhoneNumberField
from .models import Order, JobApplication, Employee, Category, Product, Service, Specialization

class CategoryForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        label="Специализации",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Category
        fields = ["name", "description", "image", "available", "specializations"]
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
        widget=forms.Select(attrs={"class": "form-control", "id": "specializationSelect"})
    )
    
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),
        label="Товары",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'id': 'productsSelect'})
    )
    
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        label="Услуги",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'id': 'servicesSelect'})
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
            "products",
            "services",
            "experience",
            "date_hired",
            "status",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].initial = "+7"
        
        if self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                if specialization_id:
                    specialization = Specialization.objects.get(id=specialization_id)
                    categories = specialization.categories.all()
                    self.fields['products'].queryset = Product.objects.filter(category__in=categories, available=True)
                    
                    selected_products = self.data.getlist('products')
                    if selected_products:
                        self.fields['services'].queryset = Service.objects.filter(
                            product__in=selected_products, available=True
                        )
            except (ValueError, TypeError, Specialization.DoesNotExist):
                pass
        if self.instance and self.instance.pk:
            if self.instance.specialization:
                categories = self.instance.specialization.categories.all()
                self.fields['products'].queryset = Product.objects.filter(category__in=categories, available=True)
                
            if self.instance.products.exists():
                self.fields['services'].queryset = Service.objects.filter(
                    product__in=self.instance.products.all(), available=True
                )


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

class OrderEditForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя клиента",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    
    last_name = forms.CharField(
        label="Фамилия клиента",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    
    middle_name = forms.CharField(
        label="Отчество клиента",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'})
    )
    

    
    phone = PhoneNumberField(
        region="RU",
        label="Телефон",
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'data-mask': '+7 (000) 000-00-00',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    
    work_description = forms.CharField(
        label="Описание требуемых работ",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите какие работы нужно выполнить'})
    )
    
    city = forms.CharField(
        label="Город",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'})
    )
    
    address = forms.CharField(
        label="Полный адрес",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица, дом, квартира'})
    )
    

    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(available=True),
        label="Категории",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),
        label="Товары",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    assigned_employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.none(),
        label="Назначенные мастера",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'middle_name', 'phone', 'work_description', 'city', 'address', 'categories', 'products', 'assigned_employees']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # При создании формы подгружаем данные из основных полей
        if self.instance and self.instance.pk:
            if not self.instance.address:
                self.fields['address'].initial = self.instance.city
            
            # Если у заказа уже есть категории, загружаем соответствующие товары и мастеров
            if self.instance.categories.exists():
                categories = self.instance.categories.all()
                self.fields['products'].queryset = Product.objects.filter(category__in=categories, available=True)
                self.fields['assigned_employees'].queryset = Employee.objects.filter(
                    specialization__categories__in=categories, 
                    available=True, 
                    status='active'
                ).distinct()
        
        # Обновляем queryset на основе POST данных
        if self.data:
            try:
                category_ids = self.data.getlist('categories')
                if category_ids:
                    self.fields['products'].queryset = Product.objects.filter(category__in=category_ids, available=True)
                    self.fields['assigned_employees'].queryset = Employee.objects.filter(
                        specialization__categories__in=category_ids, 
                        available=True, 
                        status='active'
                    ).distinct()
            except (ValueError, TypeError):
                pass

class SpecializationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(available=True),
        label="Категории",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Specialization
        fields = ['name', 'categories']
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
