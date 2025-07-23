from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Category, Product, Order
from .forms import OrderForm



class LandingView(TemplateView):
    template_name = 'main/product/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'МастерГранд'
        context['categories'] = Category.objects.filter(available=True)
        context['order_from'] = OrderForm()
        return context


class ProductListByCategory(ListView):
    model = Product
    template_name = 'main/product/product_list.html'
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
    template_name = 'main/order/modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['button_text'] = 'Оформить заказ'
        return context
    

    def form_valid(self, form):
        """Обработка успешной отправки формы через AJAX"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            order = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.',
                'order_id': order.id
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка ошибок формы через AJAX"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'form_html': render_to_string('main/order/modal.html', {
                    'form': form
                }, request=self.request)
            })
        return super().form_invalid(form)
