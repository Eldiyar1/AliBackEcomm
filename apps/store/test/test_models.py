from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.store.models import Category, Product


class TestCategoriesModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные для категории, выполняется один раз для всего класса тестов
        cls.data = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        # Получаем данные из тестового класса
        # Проверяем, что объект является экземпляром модели Category
        self.assertEqual(isinstance(self.data, Category), True)
        # Проверяем, что строковое представление объекта равно 'django'
        self.assertEqual(str(self.data), 'django')

    # def test_category_url(self):
    #     # Получаем данные из тестового класса
    #     # Генерируем URL для категории с использованием reverse
    #     response = self.client.get(reverse('base:category_list', args=[self.data.slug]))
    #     # Проверяем, что статус код ответа равен 200 (Успех)
    #     self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные для пользователя категории и продуктов
        User.objects.create_user(username='admin', password='password')
        Category.objects.create(name='django', slug='django')
        cls.data = Product.objects.create(category_id=1, created_by_id=1, title='django begin',
                                          slug='django-begin', price='20.00', image='django')

    def test_products_model_entry(self):
        # Получаем данные из тестового класса
        # Проверяем, что объект является экземпляром модели Product
        self.assertEqual(isinstance(self.data, Product), True)
        # Проверяем, что строковое представление объекта равно 'django begin'
        self.assertEqual(str(self.data), 'django begin')

    @classmethod
    def tearDownTestData(cls):
        # Удаляем только объекты, созданные в setUpTestData для данного класса
        Product.objects.all().delete()

    # def test_products_url(self):
    #     # Получаем данные из тестового класса
    #     data = self.data1
    #     # Генерируем URL для продукта с использованием reverse
    #     url = reverse('base:product_detail', args=[data.slug])
    #     # Получаем ответ по URL
    #     response = self.client.get(url)
    #     # Проверяем, что статус код ответа равен 200 (Успех)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_products_custom_manager_basic(self):
    #     # Получаем все продукты с использованием кастомного менеджера
    #     data = Product.objects.all()
    #     # Проверяем, что количество продуктов равно 1
    #     self.assertEqual(data.count(), 1)
