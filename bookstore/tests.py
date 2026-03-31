from django.test import TestCase
from .serializers import UserSerializer
from .models import User

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