from django.conf import settings
from django.db import models

from apps.store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user',
                             verbose_name='Пользователь')
    full_name = models.CharField(max_length=50, verbose_name='Полное имя')
    address1 = models.CharField(max_length=250, verbose_name='Адрес (строка 1)')
    address2 = models.CharField(max_length=250, verbose_name='Адрес (строка 2)')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    post_code = models.CharField(max_length=20, verbose_name='Почтовый код')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    total_paid = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общая сумма')
    order_key = models.CharField(max_length=200, verbose_name='Ключ заказа')
    billing_status = models.BooleanField(default=False, verbose_name='Статус выставления счета')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return str(self.id)
