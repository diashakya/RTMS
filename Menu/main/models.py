from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator



class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='specials/')
    is_vegetarian = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    customer_firstname = models.CharField(max_length=60)
    customer_lastname = models.CharField(max_length=60)
    customer_address = models.CharField(max_length=600)
    customer_email = models.EmailField(max_length=100)
    customer_dob = models.DateField()
    customer_mobileno = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.customer_email} "

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Foods(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,max_digits=8)
    image = models.ImageField(upload_to="Foods")
    is_spicy = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def __str__(self):
        return self.title
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # for registered users
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer or self.user or 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.SET_NULL, null=True, blank=True)
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.food or self.special} (Order #{self.order.id})"