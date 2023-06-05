from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    price = models.FloatField(max_length=10, null=True, blank=True)
    img = models.ImageField(upload_to="articles", null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.get_sumary
        return total

    @property
    def get_total_quantity(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.quantity
        return total


class OrderItem(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.article.name

    @property
    def get_sumary(self):
        sumary = self.quantity * self.article.price
        return sumary


class Address(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    plz = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    bundesland = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.address
