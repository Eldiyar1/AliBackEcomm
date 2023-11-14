from django.urls import path
from .views import all_products

app_name = 'core'

urlpatterns = [
    path('', all_products, name='all_products')
]
