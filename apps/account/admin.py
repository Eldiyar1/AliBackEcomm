from django.contrib import admin

from apps.account.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'is_active', 'is_staff', 'created', 'updated')
