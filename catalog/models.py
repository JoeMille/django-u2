from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house_number = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    eir_code = models.CharField(max_length=7)

    
# Category model, allowing for the creation of categories for products
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Product model, allowing for the creation of products with a description, price, and category
class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=200, default='Default Title')
    description = models.TextField()
    description2 = models.TextField(default='Default Description')
    image2 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image3 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image4 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image5 = models.ImageField(upload_to='products/', default='products/default.jpg')
    image6 = models.ImageField(upload_to='products/', default='products/default.jpg')
    price_paperback = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    price_hardback = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    BOOK_TYPES = [
        ('PB', 'Paperback'),
        ('HB', 'Hardback'),
    ]
    book_type = models.CharField(
        max_length=2,
        choices=BOOK_TYPES,
        default='PB',
    )

    def get_price(self):
        if self.book_type == 'PB':
            return self.price_paperback
        else:
            return self.price_hardback

    @property
    def price(self):
        return self.get_price()

    def __str__(self):
        return self.title

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add any other fields you need

# Basket model
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='BasketItem')

    def total_cost(self):
        return sum(item.price for item in self.basketitem_set.all())

    def get_total_price(self):
        return sum(item.price for item in self.basketitem_set.all())

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    book_type = models.CharField(max_length=2, choices=[('PB', 'Paperback'), ('HB', 'Hardback')], default='PB')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    @property  # Added property decorator
    def total_price(self):
        return self.product.get_price() * self.quantity

RATING_CHOICES = [(i, i) for i in range(1, 11)]

# Order model, allowing for the creation of orders with a user, status, created_at, and updated_at field
class Item(models.Model):
    name = models.CharField(max_length=255, default='Default Name')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        # Add more payment types as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    house = models.CharField(max_length=255, default='Default House')
    street = models.CharField(max_length=255, default='Default Street')
    city = models.CharField(max_length=255, default='Default City')
    county = models.CharField(max_length=255, default='Default County')
    eircode = models.CharField(max_length=7, default='0000000')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='credit_card')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        order_items = ", ".join(str(order_item) for order_item in self.orderitem_set.all())
        return f'Order {self.id} by {self.user.username}: {order_items}'

def get_default_product():
    return Product.objects.first().id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=get_default_product)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


# Review model, allowing for the creation of reviews for products
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(default='')

    def __str__(self):
        return f'Review for {self.product.title} by {self.user.username}'

# ContactMessage model, allowing for the creation of a contact message with an email, title, message, and created_at field
class ContactMessage(models.Model):
    email = models.EmailField(default='default@example.com')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # return the message title

# Purchase model, allowing for the creation of a purchase with a user, product, quantity, and purchase_date field

class CatalogPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Purchase of {self.product.title} by {self.user.username}'
        