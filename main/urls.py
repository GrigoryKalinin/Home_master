from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('about/', views.AboutView.as_view(), name='about_us'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('job_application/create/', views.JobApplicationCreateView.as_view(), name='job_application_create'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/<slug:employee_slug>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]