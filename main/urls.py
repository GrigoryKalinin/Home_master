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
    path('dashboard/', views.DashboardView.as_view(), name='employee_dashboard'),
    path('dashboard/all-items/', views.AllItemsListView.as_view(), name='all_items_list'),
        # Заказы
    path('dashboard/orders/', views.OrderListView.as_view(), name='order_list'),
    path('dashboard/order/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),
        # Резюме
    path('dashboard/job_applications/', views.JobApplicationListView.as_view(), name='job_application_list'),
    path('dashboard/job_application/<int:pk>/', views.JobApplicationDetailView.as_view(), name='job_application_detail'),
        # Сотрудники
    path('dashboard/specialization/create/', views.SpecializationCreateView.as_view(), name='specialization_create'),
    path('dashboard/employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('dashboard/employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('dashboard/employee/<slug:employee_slug>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('dashboard/employee/<slug:employee_slug>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
        # Категории
    path('dashboard/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('dashboard/category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('dashboard/category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('dashboard/category/<slug:slug>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
        # Продукты
    path('dashboard/product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('dashboard/product/<slug:slug>/', views.ProductDetailAdminView.as_view(), name='product_detail_admin'),
    path('dashboard/product/<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
        # Услуги
    path('dashboard/service/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('dashboard/service/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('dashboard/service/<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),


    path('<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]