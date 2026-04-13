from decimal import Decimal
from django.test import TestCase
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