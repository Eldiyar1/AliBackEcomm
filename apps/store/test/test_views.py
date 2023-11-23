from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from apps.store.models import Category, Product
from apps.store.views import products_list

@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='admin', password='password')
        self.category = Category.objects.create(name='django', slug='django')
        self.product = Product.objects.create(
            category=self.category,
            created_by=self.user,
            title='django begin',
            slug='django-begin',
            price='20.00',
            image='django'
        )

    def test_url_allowed_hosts(self):
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='localhost')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args=['django-begin']))
        self.assertEqual(response.status_code, 200)

    def test_category_list_url(self):
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = products_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>AliBack</title>', html)
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('product/django begin')
        response = products_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>AliBack</title>', html)
        self.assertEqual(response.status_code, 200)
