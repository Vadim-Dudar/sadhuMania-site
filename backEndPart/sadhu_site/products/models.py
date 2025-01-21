from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва пропозиції")
    description = models.TextField(max_length=760, verbose_name="Опис")
    size_of_foot = models.IntegerField(default=45, validators=[MinValueValidator(10), MaxValueValidator(70)], verbose_name="Розмір ноги")
    width = models.IntegerField(default=35, validators=[MinValueValidator(20)], verbose_name="Довжина")
    length = models.IntegerField(default=14, validators=[MinValueValidator(14)], verbose_name="Ширина")
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Вага")
    materials = models.TextField(max_length=100, verbose_name="Матеріали")
    equipment = models.TextField(max_length=100, verbose_name="Комплектація")
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="Ціна")
    sale_price = models.DecimalField(max_digits=11, decimal_places=1, blank=True, null=True, verbose_name="Акційна ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name="Зображення")

    def __str__(self):
        return f"Зображення для {self.product.name}"
