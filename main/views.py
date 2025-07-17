from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Category, Product



class LandingView(TemplateView):
    template_name = 'main/product/landing.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Master'
        context['categories'] = Category.objects.filter(available=True)
        return context


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id).select_related('category')[:4] # Предлагаем ещё 3 продукта из этой же самой категории
    
    return render(request, 'main/product/detail.html',
                {'category': category,
                'product': product,
                'related_products': related_products})
