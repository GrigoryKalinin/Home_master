from typing import Any
from django.db.models.base import Model as Model
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from .models import Category, Product, Order
from .forms import OrderForm



class LandingView(TemplateView):
    template_name = 'main/product/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'МастерГранд'
        context['categories'] = Category.objects.filter(available=True)
        return context


class ProductListByCategory(ListView):
    model = Product
    template_name = 'main/product/product.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(category=self.category, available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'main/order/order_from.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['button_text'] = 'Оформить заказ'
        return context