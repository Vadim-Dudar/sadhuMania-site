from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Order, Engraving
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from content.models import FooterInfo

# Create your views here.
def get_ids():
    engravings = Engraving.objects.all()
    dict_ids = []
    for engraving in engravings:
        dict_ids.append(engraving.display_id)

    return sorted(dict_ids)

class ProductDetailView(DetailView):
    model = Product  # Django автоматично знайде об'єкт за `pk` з URL
    template_name = 'ware.html'  # шлях до шаблону
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer_info'] = FooterInfo.objects.first()
        context['engraving_ids'] = get_ids()

        return context

def create_order(request):
    if request.method == 'POST':
        try:
            # Отримати JSON з тіла запиту
            data = request.body.decode('utf-8')
            data = json.loads(data)

            # Валідація даних
            required_fields = ['name_of_product', 'name', 'surname', 'phone', 'address', 'post', 'engraving', 'quantity', 'manager', 'comment']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

            # Створити об'єкт Order
            order = Order(
                product=data['name_of_product'],
                name=data['name'],
                surname=data['surname'],
                phone=data['phone'],
                address=data['address'],
                post=data['post'],
                engraving=data['engraving'],
                quantity=data['quantity'],
                manager=data['manager'],
                comment=data['comment'],
                price=Product.objects.get(name=data['name_of_product']).price*int(data['quantity']),
            )

            # Додаткова валідація (наприклад, чи email коректний)
            order.full_clean()

            # Зберегти об'єкт у базі даних
            order.save()

            # Повернути успішну відповідь
            return JsonResponse({'status': 'success', 'message': 'Order created successfully!', 'order_id': order.id})

        except ValidationError as e:
            # Повернути помилки валідації
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            # Повернути інші помилки
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def engraving_page(request):
    engravings = Engraving.objects.all().order_by('id')
    footer_info = FooterInfo.objects.first()

    context = {
        'engravings': engravings,
        'footer_info': footer_info,
    }

    return render(request, 'catalog.html', context)