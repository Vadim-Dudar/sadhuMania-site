from django.contrib import admin
from .models import Product, ProductImage


# Вбудована модель для завантаження зображень у продукт
class ProductImageInline(admin.TabularInline):  # Можна використовувати StackedInline для іншого вигляду
    model = ProductImage
    extra = 1  # Кількість порожніх полів для завантаження фото


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sale_price', 'created_at')  # Відображення в списку
    search_fields = ('name', 'materials')  # Пошук по полях
    list_filter = ('created_at',)  # Фільтр за датою створення
    inlines = [ProductImageInline]  # Додаємо inline-модель для зображень
