from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileUpdateForm, CustomPasswordChangeForm


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}! Регистрация прошла успешно.')
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and next_url != reverse_lazy('users:login'):
            return next_url
        return reverse_lazy('users:profile')
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Вы успешно вышли из системы.")
    return redirect('main:landing')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        # Игнорируем переданный pk/slug и возвращаем текущего пользователя
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Профиль: {self.object.get_full_name()}"
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        messages.success(self.request, 'Профиль успешно обновлен.')
        return reverse_lazy('users:profile')
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        return context
    

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = CustomPasswordChangeForm

    def get_success_url(self):
        messages.success(self.request, 'Пароль успешно изменен.')
        return reverse_lazy('users:profile')
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Смена пароля"
        return context