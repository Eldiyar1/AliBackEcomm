from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product',
                                 verbose_name='Категория')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator',
                                   verbose_name='Создано пользователем')
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    author = models.CharField(max_length=255, default='admin', verbose_name='автор')
    image = models.ImageField(upload_to='images/', default='images/')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=255, verbose_name='Слаг')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    is_active = models.BooleanField(default=True, verbose_name='Доступность')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
