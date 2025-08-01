from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth import get_user_model



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
    description = models.TextField(blank=True, null=True)
    is_spicy = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def __str__(self):
        return self.title
    

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('dine_in', 'Dine In'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # for registered users
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    # Order type and location fields
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='delivery')
    delivery_address = models.TextField(blank=True, null=True)  # For delivery orders
    table_number = models.CharField(max_length=10, blank=True, null=True)  # For dine-in orders
    customer_name = models.CharField(max_length=100, blank=True, null=True)  # For guest orders
    customer_phone = models.CharField(max_length=15, blank=True, null=True)  # For contact

    def __str__(self):
        return f"Order #{self.id} by {self.customer or self.user or 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.SET_NULL, null=True, blank=True)
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # price at time of order

    def save(self, *args, **kwargs):
        """Ensure price is set when saving"""
        if self.price is None or self.price == 0:
            if self.food and self.food.price:
                self.price = self.food.price
            elif self.special:
                if self.special.discounted_price:
                    self.price = self.special.discounted_price
                elif self.special.price:
                    self.price = self.special.price
                else:
                    self.price = 0
            else:
                self.price = 0
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Calculate total price for this item (price * quantity)"""
        if self.price is None:
            return 0
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.food or self.special} (Order #{self.order.id})"

class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    food = models.ForeignKey('Foods', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'food')
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f"{self.user} likes {self.food}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user or self.session_key}"

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            item_total = item.total_price
            if item_total is not None:
                total += item_total
        return total

    @property
    def total_items(self):
        total = 0
        for item in self.items.all():
            if item.quantity is not None:
                total += item.quantity
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, null=True, blank=True)
    special = models.ForeignKey(Special, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_price(self):
        if self.food and self.food.price:
            return self.food.price
        elif self.special:
            if self.special.discounted_price:
                return self.special.discounted_price
            elif self.special.price:
                return self.special.price
        return 0

    @property
    def total_price(self):
        item_price = self.item_price
        if item_price is None:
            return 0
        return item_price * self.quantity

    @property
    def item_name(self):
        if self.food:
            return self.food.title
        elif self.special:
            return self.special.name
        return "Unknown Item"

    @property
    def item_image(self):
        if self.food:
            return self.food.image
        elif self.special:
            return self.special.image
        return None

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"

    class Meta:
        unique_together = ['cart', 'food', 'special']  # Prevent duplicate items

class Contact(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"Contact from {self.name} - {self.email}"

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time}"