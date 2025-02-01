from django.shortcuts import render
from .models import CarouselImage, FooterInfo
from products.models import Product


def home_page(request):
    # Отримання активних зображень для каруселі
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('order')

    # Отримання першого запису футера (оскільки зазвичай футер містить один запис)
    footer_info = FooterInfo.objects.first()

    products = Product.objects.all()

    # Передача даних у шаблон
    context = {
        'carousel_images': carousel_images,
        'footer_info': footer_info,
        'products': products
    }
    return render(request, 'index.html', context)
