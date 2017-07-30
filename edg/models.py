from django.db import models
from django.shortcuts import reverse

class Order(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    articles = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edg:orders')