from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product

# Create your views here.

class ProductDetailView(DetailView):
    model = Product  # Django автоматично знайде об'єкт за `pk` з URL
    template_name = 'ware.html'  # шлях до шаблону
    context_object_name = 'product'
