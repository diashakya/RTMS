from django.db import models
from django.utils import timezone

# Create your models here.
class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='specials/')
    is_vegetarian = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return self.name