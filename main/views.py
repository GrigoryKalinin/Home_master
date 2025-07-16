from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all() # Получаем все категории из бд
    products = Product.objects.filter(available=True).select_related('category') # Получаем все доустпные товары из бд

    category = None # по умолчанию нет категории
    if category_slug: # если есть категория 
        category = get_object_or_404(Category, slug=category_slug) # Получаем категорию или 404 
        products = products.filter(category=category) # фильтруем продукты по категории

    return render(request, 'main/product/list.html',
                {'category': category,
                'categories': categories,
                'products': products})

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id).select_related('category')[:4] # Предлагаем ещё 3 продукта из этой же самой категории
    
    return render(request, 'main/product/detail.html',
                {'category': category,
                'product': product,
                'related_products': related_products})