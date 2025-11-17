from django.db import models

# ---------------------------------------
# Customer Model
# ---------------------------------------
class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username


# ---------------------------------------
# Restaurant Model
# ---------------------------------------
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='delivery/restaurant_images', blank=True, null=True)
    cuisine = models.CharField(max_length=200)
    rating = models.FloatField()

    def __str__(self):
        return self.name


# ---------------------------------------
# Item Model
# ---------------------------------------
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='delivery/item_images', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


# ------------------------------------------------
# Updated Cart Model USING CartItem (Correct)
# ------------------------------------------------
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    
    def total_price(self):
        return sum(ci.item.price * ci.quantity for ci in self.cart_items.all())

    def __str__(self):
        return f"{self.customer.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} × {self.quantity}"
