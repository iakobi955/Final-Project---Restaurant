from django.db import models
from django.contrib.auth.models import User

# Categories for dishes
CATEGORY_CHOICES = [
    ('Salads', 'Salads'),
    ('Soups', 'Soups'),
    ('Chicken-Dishes', 'Chicken Dishes'),
    ('Beef-Dishes', 'Beef Dishes'),
    ('Seafood-Dishes', 'Seafood Dishes'),
    ('Vegetable-Dishes', 'Vegetable Dishes'),
    ('Bits&Bites', 'Bits & Bites'),
    ('On-The-Side', 'On The Side'),
]

# Dish Model
class Dish(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dishes/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    spiciness_level = models.IntegerField(choices=[(i, str(i)) for i in range(5)])
    has_walnuts = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id}"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"
