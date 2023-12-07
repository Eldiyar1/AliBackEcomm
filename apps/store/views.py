from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def products_list(request):
    products = Product.products.all()  # products - это пользовательский менеджер(для активных продуктов)
    return render(request, 'store/home.html', {'products': products})
    # в цикле темплейта используется этот ключ products


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})
