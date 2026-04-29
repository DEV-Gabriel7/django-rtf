from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Order, User
from .serializers import OrderSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]