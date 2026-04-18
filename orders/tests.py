from django.test import TestCase
from rest_framework.test import APIClient
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


class UserViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="Gabriel", email="gabriel@email.com")

    def test_list_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_user(self):
        response = self.client.post(
            '/users/',
            {'name': 'Ana', 'email': 'ana@email.com'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Ana')

    def test_update_user(self):
        response = self.client.patch(
            f'/users/{self.user.id}/',
            {'name': 'Gabriel Ferreira'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Gabriel Ferreira')

    def test_delete_user(self):
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)


class OrderViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="Gabriel", email="gabriel@email.com")
        self.category = Category.objects.create(name="Fiction")
        self.product1 = Product.objects.create(name="Livro A", price=30.00, category=self.category)
        self.product2 = Product.objects.create(name="Livro B", price=20.00, category=self.category)
        self.order = Order.objects.create(user=self.user)
        self.order.products.set([self.product1])

    def test_list_orders(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_order(self):
        response = self.client.post(
            '/orders/',
            {'user': self.user.id, 'products': [self.product2.id]},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['products'], [self.product2.id])

    def test_update_order(self):
        response = self.client.patch(
            f'/orders/{self.order.id}/',
            {'products': [self.product1.id, self.product2.id]},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.products.count(), 2)

    def test_delete_order(self):
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 0)
