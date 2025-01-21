from django.contrib import admin
from .models import CarouselImage, FooterInfo


# Налаштування для управління каруселлю в адмінці
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    ordering = ('order',)


# Налаштування для управління футером в адмінці
@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'instagram_link')
    search_fields = ('phone', 'email')
