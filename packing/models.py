from django.core.validators import MinValueValidator
from django.db import models

POSITIVE = [MinValueValidator(0.01)]


class Product(models.Model):
    """Dimensions in cm, weight in kg."""
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    weight = models.FloatField(validators=POSITIVE)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Box(models.Model):
    """Internal dimensions in cm, max_weight in kg, cost in currency units."""
    name = models.CharField(max_length=100, unique=True)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    max_weight = models.FloatField(validators=POSITIVE)
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def volume(self):
        return self.length * self.width * self.height

    def __str__(self):
        return self.name


class Order(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
