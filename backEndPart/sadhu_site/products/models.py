from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_panel.models import SystemUser as Users
from datetime import timedelta
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва пропозиції")
    engraving = models.BooleanField(default=False, verbose_name="Можливість обрати гравіювання")
    description = models.TextField(max_length=760, verbose_name="Опис")
    size_of_foot = models.IntegerField(default=45, validators=[MinValueValidator(10), MaxValueValidator(70)], verbose_name="Розмір ноги")
    step = models.IntegerField(default=10, validators=[MinValueValidator(6), MaxValueValidator(50)], verbose_name='Крок')
    width = models.IntegerField(default=35, validators=[MinValueValidator(20)], verbose_name="Довжина")
    length = models.IntegerField(default=14, validators=[MinValueValidator(14)], verbose_name="Ширина")
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Вага")
    materials = models.TextField(max_length=100, verbose_name="Матеріали")
    equipment = models.TextField(max_length=100, verbose_name="Комплектація")
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Ціна")
    sale_price = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True, verbose_name="Акційна ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_active = models.BooleanField(default=True, verbose_name='Активний на сайті')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name="Зображення")

    def __str__(self):
        return f"Зображення для {self.product.name}"

class Available(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    count = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Кількість')
    comment = models.CharField(max_length=300, verbose_name='Коментар')
    created_at = models.DateField(auto_now_add=True, verbose_name='Cтворено')

    def __str__(self):
        return f'{self.product.name} - {self.count}'

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ім\'я')
    surname = models.CharField(max_length=100, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return f'{self.name} {self.surname} | {self.phone}'


def get_next_display_id():
    existing_ids = Engraving.objects.values_list('display_id', flat=True).order_by('display_id')

    # Якщо немає записів, почнемо з 1
    if not existing_ids:
        return 1

    # Знайти перший пропущений номер
    max_id = max(existing_ids)
    all_ids = set(range(1, max_id + 2))
    free_ids = all_ids - set(existing_ids)

    return min(free_ids) if free_ids else max_id + 1

class Engraving(models.Model):
    display_id = models.PositiveIntegerField(unique=True, default=0, verbose_name="ID")
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва")
    image = models.ImageField(upload_to='graws/', verbose_name="Гравіювання")
    upload_at = models.DateField(null=True ,editable=False ,verbose_name="Завантажено", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.display_id:  # Тільки для нових записів
            self.display_id = get_next_display_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.image}"


class Order(models.Model):
    STATUS = [
        ('received', 'Отримана'),
        ('sent', 'Відправленна'),
        ('wait', 'Чекає відправлення'),
        ('production', 'Виготовлення'),
        ('should_call', 'Уточнення'),
    ]

    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ID товару')
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ID замовника')
    manager_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ID менеджера')
    address = models.CharField(max_length=100, verbose_name='Населений пункт')
    post = models.CharField(max_length=50, verbose_name='Відділення пошти')
    engraving = models.ForeignKey(Engraving, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ID гравіювання')
    quantity = models.DecimalField(max_digits=2, decimal_places=0, verbose_name="Кількість")
    comment = models.TextField(max_length=400, verbose_name="Коментар", null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Ціна заомвлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    deadline = models.DateField(verbose_name='Дата відправлення', null=True, blank=True)
    status = models.CharField(max_length=50, default='production', choices=STATUS, verbose_name="Статус")

    def save(self, *args, **kwargs):
        if not self.deadline:
            # Якщо deadline не встановлено, встановлюємо на 3 дні вперед від поточного моменту
            self.deadline = timezone.now().date() + timedelta(days=3)
        super().save(*args, **kwargs)

    def __str__(self):
        product_name = self.product_id.name if self.product_id else "—"
        return f"[{self.id}] {product_name} - {self.quantity} | {self.status} | {self.price} грн."
