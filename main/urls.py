from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('about/', views.AboutView.as_view(), name='about_us'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]