from django.contrib import admin
from .models import SystemUser

# Register your models here.
@admin.register(SystemUser)
class SystemUsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'access_level')
    list_filter = ('access_level',)
    search_fields = ('user_id', 'name',)
