from django.db import models
from django.conf import settings
from main_site.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum

class Review(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_published = models.BooleanField(default=False)

    #when changing review (in admin panel or by user), update average Product's rating
    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.agregate_obj = Review.objects.filter(item=self.item, is_published=True)
        self.save_average = self.item
        if self.agregate_obj.count()>=1:
            self.save_average.average_rating = round(self.agregate_obj.aggregate(Sum('rating'))['rating__sum'] / self.agregate_obj.count(), 2)
            self.save_average.reviews_count = self.agregate_obj.count()
        else:
            self.save_average.average_rating=0
            self.save_average.reviews_count = 0
        self.save_average.save()
