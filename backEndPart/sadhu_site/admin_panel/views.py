import os
import pandas as pd
import matplotlib.pyplot as plt

from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from .models import SystemUser, Expense, MonthlyStats
from products.models import Order

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
    return render(request, 'crm/dashboard.html', {
        'user': user,
        'revenue': revenue,
        'expenses': expenses,
        'roi': roi,
        'cr': cr,
        'cpl': cpl,
        'asoop': asoop,
        'today': orders_today,
    })
