from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from autoriz.models import MyUser
from django.core.validators import MinValueValidator
from decimal import Decimal
from categories.models import Category

# class Category(models.Model):
#     name = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, db_index=True, unique=True)
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(_('description'), default=None)
    # stock = models.PositiveIntegerField()
    designer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    is_legally = models.BooleanField(default=True)
    available = models.BooleanField(_('available'), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0)
    reviews_count = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main_site:product', kwargs={'pk': self.pk})

class Delivery(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type

class DetailProduce(models.Model):
    producer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    days = models.PositiveSmallIntegerField()
    shipping = models.ManyToManyField(Delivery)

class OurProfit(models.Model):
    profit = models.PositiveSmallIntegerField(max_length=100, default=8)

    def __str__(self):
        return 'Our Profit'