from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy

from .models import Category, Product, Order
from .forms import OrderForm


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

        return context


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


# class ReviewCreateView(LoginRequiredMixin, CreateView):
#     model = Review
#     form_class = ReviewForm
#     template_name = "main/review/create.html"
#     success_url = reverse_lazy("main:landing")
#     login_url = "/admin/login/"  # или создайте свою страницу входа

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
