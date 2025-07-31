from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.urls import reverse_lazy

from datetime import date

from .models import Category, Product, Service, Order, JobApplication, Employee
from .forms import OrderForm, JobApplicationForm, EmployeeForm, CategoryForm, ProductForm, ServiceForm


class LandingView(TemplateView):
    template_name = "main/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "МастерГранд"
        context["categories"] = Category.objects.filter(available=True)
        context["order_from"] = OrderForm()
        return context


class AboutView(TemplateView):
    template_name = "main/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_from"] = OrderForm()  
        return context

# Категории (для сотрудников)
# TODO доработать

class CategoryListView(ListView):
    model = Category
    template_name = "main/private/category/category_list.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        queryset = Category.objects.all().order_by('name')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        available = self.request.GET.get('available')
        if available == 'true':
            queryset = queryset.filter(available=True)
        elif available == 'false':
            queryset = queryset.filter(available=False)
            
        return queryset

class CategoryDetailView(DetailView):
    model = Category
    template_name = "main/private/category/category_detail.html"
    context_object_name = "category"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        
        # Получаем товары категории с фильтрацией
        products = Product.objects.filter(category=category).order_by('name')
        
        search = self.request.GET.get('search')
        if search:
            products = products.filter(name__icontains=search)
            
        available = self.request.GET.get('available')
        if available == 'true':
            products = products.filter(available=True)
        elif available == 'false':
            products = products.filter(available=False)
            
        context['products'] = products
        context['search_query'] = search or ''
        context['current_available'] = available or ''
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "main/private/category/category_form.html"
    success_url = reverse_lazy("main:category_list")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "main/private/category/category_form.html"
    success_url = reverse_lazy("main:category_list")


# Продукты (для пользователей)
class ProductListByCategory(ListView):
    model = Product
    template_name = "main/product/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        return Product.objects.filter(category=self.category, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["order_from"] = OrderForm()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        category_slug = self.kwargs["category_slug"]
        product_slug = self.kwargs["product_slug"]

        queryset = queryset.select_related("category")

        product = get_object_or_404(
            queryset,
            category__slug=category_slug,
            slug=product_slug,
            available=True,
        )
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context["title"] = product.name
        context["description"] = product.description
        context["category"] = product.category
        context["order_from"] = OrderForm()

        return context

# Продукты (для сотрудников)
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "main/private/product/product_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:category_detail", kwargs={'slug': self.object.category.slug})
    
    def get_initial(self):
        initial = super().get_initial()
        category_slug = self.request.GET.get('category')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                initial['category'] = category
            except Category.DoesNotExist:
                pass
        return initial

class ProductDetailAdminView(DetailView):
    model = Product
    template_name = "main/private/product/product_detail.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Получаем услуги товара с фильтрацией
        services = Service.objects.filter(product=product).order_by('name')
        
        search = self.request.GET.get('search')
        if search:
            services = services.filter(name__icontains=search)
            
        available = self.request.GET.get('available')
        if available == 'true':
            services = services.filter(available=True)
        elif available == 'false':
            services = services.filter(available=False)
            
        context['services'] = services
        context['search_query'] = search or ''
        context['current_available'] = available or ''
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "main/private/product/product_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:category_detail", kwargs={'slug': self.object.category.slug})

# Услуги (для сотрудников)
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "main/private/service/service_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:product_detail_admin", kwargs={'slug': self.object.product.slug})
    
    def get_initial(self):
        initial = super().get_initial()
        product_slug = self.request.GET.get('product')
        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug)
                initial['product'] = product
            except Product.DoesNotExist:
                pass
        return initial

class ServiceDetailView(DetailView):
    model = Service
    template_name = "main/private/service/service_detail.html"
    context_object_name = "service"

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "main/private/service/service_form.html"
    
    def get_success_url(self):
        return reverse_lazy("main:product_detail_admin", kwargs={'slug': self.object.product.slug})

# Сотрудники (для сотрудников)
class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "main/private/employee_create.html"
    success_url = reverse_lazy("main:employee_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление сотрудника"
        context["button_text"] = "Добавить сотрудника"
        return context

class EmployeeListView(ListView):
    model = Employee
    template_name = "main/private/employee_list.html"
    context_object_name = "employees"
    
    def get_queryset(self):
        queryset = Employee.objects.all().order_by('last_name')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(city__icontains=search) |
                Q(specialization__icontains=search)
            )
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Employee.STATUS_CHOICES
        return context

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "main/private/employee_create.html"
    slug_url_kwarg = 'employee_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование сотрудника"
        context["button_text"] = "Сохранить изменения"
        return context

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "main/private/employee_detail.html"
    context_object_name = "employee"
    slug_url_kwarg = 'employee_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.object
        
        # Стаж в компании
        if employee.date_hired:
            today = date.today()
            years = today.year - employee.date_hired.year
            if today.month < employee.date_hired.month or (today.month == employee.date_hired.month and today.day < employee.date_hired.day):
                years -= 1
            context['company_experience'] = years
        
        return context

# Заявки для пользователей
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "main/order/order_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["button_text"] = "Оформить заказ"
        return context

    def form_valid(self, form):
        form.instance.created_by_client = True
        """Обработка успешной отправки формы через AJAX"""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            order = form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.",
                    "order_id": order.id,
                }
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка ошибок формы через AJAX"""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "errors": form.errors,
                    "form_html": render_to_string(
                        "main/order/order_create.html",
                        {"form": form},
                        request=self.request,
                    ),
                }
            )
        return super().form_invalid(form)

# Заявки для сотрудников
class OrderListView(ListView):
    model = Order
    template_name = "main/private/order_list.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        queryset = Order.objects.all().order_by('-date_created')
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone__icontains=search) |
                Q(city__icontains=search)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        return context

class OrderStatusUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({
                'success': True,
                'new_status': order.get_status_display()
            })
        
        return JsonResponse({'success': False})

# Резюме для пользователей
class JobApplicationCreateView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = "main/job_application/job_application_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Анкета мастера"
        context["button_text"] = "Отправить анкету"
        context["order_from"] = OrderForm()
        return context

    def form_valid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            application = form.save()
            return JsonResponse({
                "success": True,
                "message": "Анкета успешно отправлена! Мы рассмотрим вашу заявку и свяжемся с вами.",
                "application_id": application.id,
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors,
                "form_html": render_to_string(
                    "main/job_application/job_application_create.html",
                    {"form": form},
                    request=self.request,
                ),
            })
        return super().form_invalid(form)

# Резюме (для сотрудников)
class JobApplicationListView(ListView):
    model = JobApplication
    template_name = "main/private/job_application_list.html"
    context_object_name = "applications"
    
    def get_queryset(self):
        queryset = JobApplication.objects.all().order_by('-date_created')
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(city__icontains=search) |
                Q(specialization__icontains=search)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = JobApplication.STATUS_CHOICES
        return context

class JobApplicationDetailView(DetailView):
    model = JobApplication
    template_name = "main/private/job_application_detail.html"
    context_object_name = "application"
    
    def post(self, request, *args, **kwargs):
        application = self.get_object()
        new_status = request.POST.get('status')
        
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            
        return JsonResponse({
            'success': True,
            'new_status': application.get_status_display()
        })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = JobApplication.STATUS_CHOICES
        return context

# class ReviewCreateView(LoginRequiredMixin, CreateView):
#     model = Review
#     form_class = ReviewForm
#     template_name = "main/review/create.html"
#     success_url = reverse_lazy("main:landing")
#     login_url = "/admin/login/"  # или создайте свою страницу входа

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
