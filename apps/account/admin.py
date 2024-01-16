from django.contrib import admin

from apps.account.models import Customer, Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'is_staff', 'created', 'updated')
    list_editable = ('is_active', 'is_staff')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'full_name', 'phone', 'postcode', 'town_city', 'default')
    list_filter = ('customer', 'town_city', 'default')