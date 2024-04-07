from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    balance = models.DecimalField('account balance', default=0.0, max_digits=65, decimal_places=3)

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=65, decimal_places=3)
    quantity = models.IntegerField()
    image = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    if quantity == 0:
        pass
    
    def __str__(self) -> str:
        return f'Product: {self.name}'
    
class Transaction(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=65, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Seller: {self.seller} <==> Buyer: {self.buyer}'

class ShilingPackages(models.Model):
    pass