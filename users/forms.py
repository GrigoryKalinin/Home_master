from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags

from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Email'})
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'})
    )
    phone = PhoneNumberField(
        region="RU",
        label="Ваш телефон",
        widget=forms.TextInput(attrs={"placeholder": "+7 (999) 123-45-67", "class": "form-control phone-mask", "data-mask": "+7 (000) 000-00-00", "autocomplete": "off",  "inputmode": "tel"}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
    )
    marketing_consent1 = forms.BooleanField(label='Согласие на рассылку', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    marketing_consent2 = forms.BooleanField(label='Согласие на обработку персональных данных', required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'marketing_consent1', 'marketing_consent2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует')
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.marketing_consent1 = self.cleaned_data['marketing_consent1']
        user.marketing_consent2 = self.cleaned_data['marketing_consent2']
        if commit:
            user.save()
        return user
    

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Email', 'autocomplete': 'email', 'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                self.user_cache = authenticate(self.request, email=email, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError('Неверный логин или пароль')
                self.confirm_login_allowed(self.user_cache)
            except forms.ValidationError:
                raise
        return self.cleaned_data
    

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'address', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Аватар'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует')
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email

        for field in ['first_name', 'last_name', 'city', 'address']:
            if field in cleaned_data and cleaned_data[field]:
                cleaned_data[field] = strip_tags(str(cleaned_data.get(field, '')))

        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'})
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'})
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение нового пароля'})
    )