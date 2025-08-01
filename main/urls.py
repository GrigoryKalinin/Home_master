from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('about/', views.AboutView.as_view(), name='about_us'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('job/', views.JobApplicationView.as_view(), name='job_application'),
    path('job/form', views.JobApplicationCreateFormView.as_view(), name='job_application_form'),

    # Управление
        # Заказы
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),
        # Резюме
    path('job_applications/', views.JobApplicationListView.as_view(), name='job_application_list'),
    path('job_application/<int:pk>/', views.JobApplicationDetailView.as_view(), name='job_application_detail'),
        # Сотрудники
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/<slug:employee_slug>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<slug:employee_slug>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
        # Категории
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug:slug>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
        # Продукты
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/', views.ProductDetailAdminView.as_view(), name='product_detail_admin'),
    path('product/<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
        # Услуги
    path('service/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('service/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('service/<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),


    path('<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]