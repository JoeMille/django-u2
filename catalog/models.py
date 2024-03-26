from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Basket model
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='BasketItem')

    def total_cost(self):
        return sum(item.total_price() for item in self.basketitem_set.all())
    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.basketitem_set.all())

# Basket model, allowing for the creation of a basket for a user
class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

RATING_CHOICES = [(i, i) for i in range(1, 11)]

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