from django.urls import path

from .views import category_list, product_detail, products_list

app_name = 'store'

urlpatterns = [
    path('', products_list, name='products_list'),
    path('shop/<slug:slug>', product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', category_list, name='category_list'),
]
