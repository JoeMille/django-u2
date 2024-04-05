from django.contrib import admin
from .models import Category, Product, Basket, BasketItem, Review, ContactMessage, CatalogPurchase

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'description2', 'price', 'image', 'image2', 'image3', 'image4')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'message', 'created_at')  # fields to display in the list view

@admin.register(CatalogPurchase)
class PurchaseAdmin(admin.ModelAdmin):
    # your admin configuration here
    list_display = ['id', 'user', 'product', 'quantity', 'purchase_date']

admin.site.register(ContactMessage, ContactMessageAdmin)  # register ContactMessageAdmin with ContactMessage
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # register ProductAdmin with Product
admin.site.site_header = 'Cosmic Commerce Admin Portal'
admin.site.site_title = 'Admin Operations'