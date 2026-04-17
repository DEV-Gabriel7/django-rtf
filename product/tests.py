from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Fiction", description="Livros de ficção")

        self.assertEqual(category.name, "Fiction")
        self.assertEqual(category.description, "Livros de ficção")


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Fiction")

    def test_create_product(self):
        product = Product.objects.create(
            name="Livro A",
            description="Descrição do Livro A",
            price=49.90,
            category=self.category,
        )

        self.assertEqual(product.name, "Livro A")
        self.assertEqual(product.category, self.category)
        self.assertEqual(float(product.price), 49.9)
        self.assertEqual(Decimal(str(product.price)).quantize(Decimal('0.00')), Decimal("49.90"))


class CategorySerializerTest(TestCase):

    def test_serializer_valid(self):
        data = {
            "name": "Fiction",
            "description": "Livros de ficção"
        }

        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Fiction")

    def test_serializer_valid(self):
        data = {
            "name": "Livro A",
            "description": "Retorno",
            "price": "49.90",
            "category": self.category.id,
        }

        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class CategoryViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Fiction", description="Livros de ficção")

    def test_list_categories(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        response = self.client.post(
            '/categories/',
            {'name': 'Science', 'description': 'Livros de ciência'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Science')

    def test_update_category(self):
        response = self.client.patch(
            f'/categories/{self.category.id}/',
            {'description': 'Novo texto'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.description, 'Novo texto')

    def test_delete_category(self):
        response = self.client.delete(f'/categories/{self.category.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)


class ProductViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Fiction")
        self.product = Product.objects.create(
            name='Livro A',
            description='Descrição do Livro A',
            price=49.90,
            category=self.category,
        )

    def test_list_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        response = self.client.post(
            '/products/',
            {
                'name': 'Livro B',
                'description': 'Descrição do Livro B',
                'price': '59.90',
                'category': self.category.id,
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Livro B')

    def test_update_product(self):
        response = self.client.patch(
            f'/products/{self.product.id}/',
            {'price': '39.90'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.price), '39.90')

    def test_delete_product(self):
        response = self.client.delete(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)
