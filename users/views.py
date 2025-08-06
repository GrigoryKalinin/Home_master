from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileUpdateForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from main.forms import OrderForm
from main.models import Order


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
        context["order_from"] = OrderForm()
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
        context["order_from"] = OrderForm()
        return context


class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'users/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        # Фильтруем заказы по номеру телефона пользователя, если он указан
        if self.request.user.phone:
            return Order.objects.filter(phone=self.request.user.phone).order_by('-date_created')
        return Order.objects.none()

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мои заказы"
        context["order_from"] = OrderForm()
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
        context["order_from"] = OrderForm()
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
        context["order_from"] = OrderForm()
        return context
    

class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()
        return context

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()
        return context

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()
        return context

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()
        return context


class AjaxLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            login(self.request, form.get_user())
            return JsonResponse({
                'success': True,
                'message': f'Добро пожаловать, {form.get_user().get_full_name()}!',
                'redirect_url': self.get_success_url()
            })
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = dict(form.errors)
            if form.non_field_errors():
                errors['__all__'] = form.non_field_errors()
            return JsonResponse({
                'success': False,
                'errors': errors
            })
        return super().form_invalid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and next_url != reverse_lazy('users:login'):
            return next_url
        if self.request.user.is_staff:
            return reverse_lazy('main:employee_dashboard')
        return reverse_lazy('users:profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()
        return context