from django.db import models
from product.models import Product

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(product.price for product in self.products.all())

    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"
