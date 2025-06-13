import os
import pandas as pd
import matplotlib.pyplot as plt

from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import SystemUser, Expense, MonthlyStats
from products.models import Order, Available
from django.db.models import Count
from content.models import CarouselImage, FooterInfo
from django.http import JsonResponse
from .forms import CarouselImageForm
from django.views.decorators.csrf import csrf_exempt

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = SystemUser.objects.get(login=username)
            if check_password(password, user.password):
                request.session['system_user_id'] = user.id
                return render_dashboard(request)
            else:
                return render(request, 'crm/login.html', {'error': 'Невірний пароль'})
        except SystemUser.DoesNotExist:
            return render(request, 'crm/login.html', {'error': 'Користувача не знайдено'})

    if request.session.get('system_user_id'):
        return render_dashboard(request)

    return render(request, 'crm/login.html')

def render_dashboard(request):
    user_id = request.session.get('system_user_id')
    if not user_id:
        return render(request, 'crm/login.html')

    user = SystemUser.objects.get(id=user_id)

    # ================================================
    # 1. Генерація графіка ASOOP
    orders = Order.objects.exclude(deadline__isnull=True)

    asoop = 0  # значення для KPI
    if orders.exists():
        df = pd.DataFrame.from_records(
            orders.values('id', 'created_at', 'deadline')
        )

        df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
        df['deadline'] = pd.to_datetime(df['deadline'], utc=True)
        df['asoop_days'] = (df['deadline'] - df['created_at']).dt.total_seconds() / (60 * 60 * 24)
        df['month'] = df['created_at'].dt.to_period('M')

        # Для KPI
        asoop = round(df['asoop_days'].mean(), 1)

        # Для графіка
        order_counts = df.groupby('month')['id'].count()
        avg_asoop = df.groupby('month')['asoop_days'].mean()

        # Побудова графіка
        fig, ax1 = plt.subplots(figsize=(10, 6))
        color1 = '#3498db'
        ax1.bar(order_counts.index.astype(str), order_counts.values, color=color1)
        ax1.set_xlabel('Місяць')
        ax1.set_ylabel('Кількість замовлень', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)

        ax2 = ax1.twinx()
        color2 = '#e74c3c'
        ax2.plot(avg_asoop.index.astype(str), avg_asoop.values, color=color2, marker='o', linewidth=2)
        ax2.set_ylabel('Середній ASOOP (днів)', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)

        plt.title('Кількість замовлень та середній час виконання (ASOOP)')
        ax1.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()

        chart_path = os.path.join(settings.BASE_DIR, 'assets/generated/chart.png')
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.savefig(chart_path)
        plt.close()

    # ================================================
    # 2. KPI блоки (ROI, CR, CPL)
    now = timezone.now()
    start_of_month = now.replace(day=1)

    # Виручка за поточний місяць
    revenue = Order.objects.filter(created_at__gte=start_of_month).aggregate(total=Sum('price'))['total'] or 0

    # Загальні витрати
    expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

    # ROI
    roi = round(((revenue - expenses) / expenses * 100), 2) if expenses else 0

    # Monthly stats
    month_name = now.strftime('%B %Y')
    monthly = MonthlyStats.objects.filter(month=month_name).first()

    if monthly:
        leads = monthly.leads or 0
        conversions = monthly.conversions or 0
        cr = round((conversions / leads * 100), 2) if leads else 0
        cpl = round((expenses / leads), 2) if leads else 0
    else:
        cr = 0
        cpl = 0

    orders_today = Order.objects.filter(deadline=now.date())
    # ================================================

    # Цікавлять тільки замовлення зі статусами "в роботі"
    working_statuses = ['should_call', 'production', 'wait', 'sent']
    orders = Order.objects.filter(status__in=working_statuses)

    # Групуємо по статусу
    status_counts = orders.values('status').annotate(count=Count('id'))

    # Перетворюємо в словник
    status_dict = {item['status']: item['count'] for item in status_counts}

    # Загальна кількість замовлень у роботі
    total = sum(status_dict.values()) or 1  # захист від ділення на 0

    # Розрахунок відсотків
    percentage_dict = {
        'should_call': round(status_dict.get('should_call', 0) / total * 100, 2),
        'production': round(status_dict.get('production', 0) / total * 100, 2),
        'wait': round(status_dict.get('wait', 0) / total * 100, 2),
        'sent': round(status_dict.get('sent', 0) / total * 100, 2),
    }

    return render(request, 'crm/dashboard.html', {
        'user': user,
        'revenue': revenue,
        'expenses': expenses,
        'roi': roi,
        'cr': cr,
        'cpl': cpl,
        'asoop': asoop,
        'today': orders_today,
        'percentage': percentage_dict,
    })

def logout_view(request):
    request.session.flush()
    return redirect('login_page')

def edit_site(request):
    user_id = request.session.get('system_user_id')
    if not user_id:
        return render(request, 'crm/login.html')

    user = SystemUser.objects.get(id=user_id)
    footer = FooterInfo.objects.first()
    return render(request, 'crm/editSite.html', {
        'user': user,
        'cards': CarouselImage.objects.all(),
        'footer': footer
    })

def add_carousel_slide_ajax(request):
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save()
            return JsonResponse({'success': True, 'new_id': slide.id})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def delete_carousel(request):
    if request.method == 'POST':
        slide_id = request.POST.get('id')
        try:
            slide = CarouselImage.objects.get(id=slide_id)
            slide.delete()
            return JsonResponse({'success': True})
        except CarouselImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Slide not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_carousel(request):
    if request.method == 'POST':
        slide_id = request.POST.get('id')
        try:
            slide = CarouselImage.objects.get(id=slide_id)
            slide.title = request.POST.get('title')
            slide.button = request.POST.get('button')
            slide.slide_type = request.POST.get('slide_type')
            slide.order = int(request.POST.get('order'))

            if 'image' in request.FILES:
                slide.image = request.FILES['image']

            slide.save()
            return JsonResponse({'success': True})
        except CarouselImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_footer(request):
    if request.method == 'POST':
        try:
            footer = FooterInfo.objects.first()
            if not footer:
                return JsonResponse({'success': False, 'error': 'FooterInfo not found'}, status=404)

            footer.instagram = request.POST.get('instagram')
            footer.phone = request.POST.get('phone')
            footer.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def avalybility(request):
    user_id = request.session.get('system_user_id')
    if not user_id:
        return render(request, 'crm/login.html')

    user = SystemUser.objects.get(id=user_id)
    footer = FooterInfo.objects.first()

    # !!! додай передачу списку продуктів (для <datalist>)
    from products.models import Product

    return render(request, 'crm/availybility.html', {
        'user': user,
        'availybilyty': Available.objects.all(),
        'products': Product.objects.all(),
        'footer': footer
    })

@csrf_exempt
def add_availability_ajax(request):
    if request.method == 'POST':
        product_name = request.POST.get('product')
        count = request.POST.get('count')
        comment = request.POST.get('comment')

        try:
            from products.models import Product
            product = Product.objects.get(name=product_name)
            avail = Available.objects.create(product=product, count=count, comment=comment)
            return JsonResponse({
                'success': True,
                'new_id': avail.id,
                'product_name': product.name,
                'count': avail.count,
                'comment': avail.comment
            })
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_availability_ajax(request):
    if request.method == 'POST':
        avail_id = request.POST.get('id')
        try:
            avail = Available.objects.get(id=avail_id)
            from products.models import Product
            product = Product.objects.get(name=request.POST.get('product'))
            avail.product = product
            avail.count = request.POST.get('count')
            avail.comment = request.POST.get('comment')
            avail.save()
            return JsonResponse({'success': True})
        except (Available.DoesNotExist, Product.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Item or product not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_availability_ajax(request):
    if request.method == 'POST':
        availability_id = request.POST.get('id')
        try:
            avail = Available.objects.get(id=availability_id)
            avail.delete()
            return JsonResponse({'success': True})
        except Available.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

