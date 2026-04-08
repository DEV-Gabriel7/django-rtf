from django.test import TestCase
from .models import User, Order
from .serializers import UserSerializer, OrderSerializer
from product.models import Category, Product


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
