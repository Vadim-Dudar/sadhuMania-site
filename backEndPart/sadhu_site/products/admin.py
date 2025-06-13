from fileinput import close

from django.contrib import admin
from .models import Product, ProductImage, Order, Engraving, Customer, Available


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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display — колонки, що будуть показані в адмінці
    list_display = (
        'get_product_name',   # Назва товару
        'get_customer_phone', # Телефон клієнта
        'get_manager_name',   # Менеджер
        'created_at',         # Дата замовлення
        'price',              # Ціна
        'status',             # Статус
    )

    # Поля, які можна редагувати прямо зі списку
    list_editable = ('status',)

    # Поля для пошуку
    search_fields = (
        'product_id__name',
        'customer_id__phone',
    )

    # Фільтри праворуч
    list_filter = ('created_at', 'status')

    # Метод: Назва товару
    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else "—"
    get_product_name.short_description = 'Товар'

    # Метод: Телефон клієнта
    def get_customer_phone(self, obj):
        return obj.customer_id.phone if obj.customer_id else "—"
    get_customer_phone.short_description = 'Телефон'

    # Метод: Менеджер
    def get_manager_name(self, obj):
        return obj.manager_id.name if obj.manager_id else "—"
    get_manager_name.short_description = 'Менеджер'

@admin.register(Engraving)
class EngravingAdmin(admin.ModelAdmin):
    list_display = ('display_id', 'name', 'upload_at')
    search_fields = ('name',)
    list_filter = ('upload_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('phone',)

@admin.register(Available)
class AvailableAdmin(admin.ModelAdmin):
    list_display = ('product', 'comment', 'count')
    search_fields = ('product',)
