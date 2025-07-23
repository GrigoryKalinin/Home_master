from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list'),
]