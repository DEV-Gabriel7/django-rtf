from decimal import Decimal
from django.test import TestCase
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer
from .models import User, Category, Product, Order

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create(
            name="Gabriel",
            email="gabriel@email.com"
        )

        self.assertEqual(user.name, "Gabriel")
        self.assertEqual(user.email, "gabriel@email.com")



class UserSerializerTest(TestCase):

    def test_serializer_valid(self):
        data = {
            "name": "Gabriel",
            "email": "gabriel@email.com"
        }

        serializer = UserSerializer(data=data)

        self.assertTrue(serializer.is_valid())


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


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="Gabriel", email="gabriel@email.com")
        self.category = Category.objects.create(name="Fiction")
        self.product1 = Product.objects.create(name="Livro A", price=30.00, category=self.category)
        self.product2 = Product.objects.create(name="Livro B", price=20.00, category=self.category)

    def test_create_order(self):
        order = Order.objects.create(user=self.user)
        order.products.set([self.product1, self.product2])

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.products.count(), 2)
        self.assertEqual(order.total, 50.00)


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


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="Gabriel", email="gabriel@email.com")
        self.category = Category.objects.create(name="Fiction")
        self.product = Product.objects.create(name="Livro A", price=30.00, category=self.category)

    def test_serializer_valid(self):
        order = Order.objects.create(user=self.user)
        order.products.set([self.product])

        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(serializer.data["products"], [self.product.id])