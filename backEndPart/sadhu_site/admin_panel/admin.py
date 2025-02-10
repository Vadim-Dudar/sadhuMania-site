from django.contrib import admin
from .models import BotUsers

# Register your models here.
@admin.register(BotUsers)
class BotUsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'access_level')
    list_filter = ('access_level',)
    search_fields = ('user_id', 'name',)
