from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.store.models import Category, Product


class TestCategoriesModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        self.assertEqual(isinstance(self.data, Category), True)
        self.assertEqual(str(self.data), 'django')

    def test_category_url(self):
        response = self.client.get(reverse('store:category_list', args=[self.data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='admin', password='password')
        Category.objects.create(name='django', slug='django')
        cls.data = Product.objects.create(category_id=1, created_by_id=1, title='django begin',
                                          slug='django-begin', price='20.00', image='django')

    def test_products_model_entry(self):
        self.assertEqual(isinstance(self.data, Product), True)
        self.assertEqual(str(self.data), 'django begin')

    def test_products_url(self):
        url = reverse('store:product_detail', args=[self.data.slug])
        self.assertEqual(url, '/product/django-begin')
        response = self.client.post(
            reverse('store:product_detail', args=[self.data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        data = Product.products.all()
        self.assertEqual(data.count(), 1)
