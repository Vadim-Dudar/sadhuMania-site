from django.db.models.fields import return_None
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Order, Engraving, Customer, Users
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from content.models import FooterInfo
from telegram_bot.bot_runner import send_order_notification
from asgiref.sync import async_to_sync


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
            print(data)

            # Валідація даних
            required_fields = ['name_of_product', 'name', 'surname', 'phone', 'address', 'post', 'engraving', 'quantity', 'manager', 'comment']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)

            # Створити об'єкт Order
            product = Product.objects.get(name=data['name_of_product'])
            if data['engraving'] != '1':
                engraving = Engraving.objects.get(display_id=data['engraving'][1:])
            else:
                engraving = None

            customer, _ = Customer.objects.get_or_create(
                name=data['name'],
                surname=data['surname'],
                phone=data['phone']
            )

            order = Order(
                product_id=product,
                customer_id=customer,
                manager_id=Users.objects.get(name='Вадім Дудар'),
                address=data['address'],
                post=data['post'],
                engraving=engraving,
                quantity=data['quantity'],
                comment=data['comment'],
                status='should_call' if data['manager'] else 'production',
                price=product.price * int(data['quantity']) + (200 if data['engraving'] != '1' else 0)
            )

            # Додаткова валідація (наприклад, чи email коректний)
            order.full_clean()

            # Зберегти об'єкт у базі даних
            order.save()

            async_to_sync(send_order_notification)(order)

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