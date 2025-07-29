from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm
from .models import User


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
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
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    
    



class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user