from django.contrib import admin

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'slug', 'price',
        'in_stock', 'created', 'updated'
    )
    list_filter = ('in_stock', 'is_active')
    list_editable = ('price', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    readonly_fields = ('created', 'updated')
    list_per_page = 5
    ordering = ('-created',)
