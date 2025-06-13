from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class SystemUser(models.Model):
    SLIDE_TYPE_CHOICES = [
        ('manager', 'Менеджер'),
        ('admin', 'Адміністратор'),
        ('worker', 'Оператор виготовлення'),
    ]

    name = models.CharField(max_length=255, verbose_name="Ім'я")
    login = models.CharField(max_length=20, unique=True,  verbose_name='Логін')
    password = models.CharField(max_length=128, default='0000', verbose_name='Пароль')
    access_level = models.CharField(
        max_length=12,
        choices=SLIDE_TYPE_CHOICES,
        default='admin',
        verbose_name="Рівень доступу"
    )
    user_id = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name="ID користувача")

    def save(self, *args, **kwargs):
        # Перевіряємо, чи пароль уже захешований
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'[{self.user_id}] {self.name} з рівнем досткпу {self.access_level}'


class MonthlyStats(models.Model):
    month = models.CharField(max_length=20, verbose_name='Місяць')
    leads = models.PositiveIntegerField(verbose_name='Ліди')
    conversions = models.PositiveIntegerField(verbose_name='Конверсії')
    sales_plan = models.PositiveIntegerField(verbose_name='План продажу')
    planned_budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Планований бюджет')

    def __str__(self):
        return f"{self.month} – Ліди: {self.leads}, Конверсії: {self.conversions}"

class ExpenseType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва виду витрат')

    def __str__(self):
        return self.name

class Expense(models.Model):
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, verbose_name='Вид витрат')
    description = models.TextField(verbose_name='Опис')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сума')

    def __str__(self):
        return f"{self.expense_type.name} – {self.amount} грн"

