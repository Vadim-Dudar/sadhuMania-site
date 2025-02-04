from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва пропозиції")
    engraving = models.BooleanField(default=False, verbose_name="Можливість обрати гравіювання")
    description = models.TextField(max_length=760, verbose_name="Опис")
    size_of_foot = models.IntegerField(default=45, validators=[MinValueValidator(10), MaxValueValidator(70)], verbose_name="Розмір ноги")
    width = models.IntegerField(default=35, validators=[MinValueValidator(20)], verbose_name="Довжина")
    length = models.IntegerField(default=14, validators=[MinValueValidator(14)], verbose_name="Ширина")
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Вага")
    materials = models.TextField(max_length=100, verbose_name="Матеріали")
    equipment = models.TextField(max_length=100, verbose_name="Комплектація")
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Ціна")
    sale_price = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True, verbose_name="Акційна ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name="Зображення")

    def __str__(self):
        return f"Зображення для {self.product.name}"

class Order(models.Model):
    product = models.CharField(max_length=255, verbose_name="Назва пропозиції")
    name = models.CharField(max_length=100, verbose_name='Ім\'я')
    surname = models.CharField(max_length=100, verbose_name='Прізвище')
    phone = models.CharField(max_length=50, verbose_name='Номер телефону')
    address = models.CharField(max_length=100, verbose_name='Населений пункт')
    post = models.CharField(max_length=50, verbose_name='Відділення пошти')
    engraving = models.CharField(default=None ,max_length=50 ,verbose_name='Грвіювання')
    quantity = models.DecimalField(max_digits=2, decimal_places=0, verbose_name="Кількість")
    manager = models.BooleanField(default=True ,verbose_name="Необхідно зателефонувати")
    comment = models.TextField(max_length=400, verbose_name="Коментар", null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Ціна заомвлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    sent = models.BooleanField(default=False, verbose_name="Відправлена")

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.quantity} | {self.manager} | {self.price} грн."

def get_next_display_id():
    # Знайти всі існуючі display_id
    existing_ids = Engraving.objects.values_list('display_id', flat=True).order_by('display_id')

    # Якщо немає записів, почнемо з 1
    if not existing_ids:
        return 1

    # Знайти перший пропущений номер
    max_id = max(existing_ids)
    all_ids = set(range(1, max_id + 2))  # +2 для випадку, коли всі номери заповнені
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
