from django import forms
from django.db import models
from django.contrib import admin
from .models import Category, Product, Basket, BasketItem, Review, ContactMessage, CatalogPurchase

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    description2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Product
        exclude = ['category']

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'title', 'description_truncated', 'description2_truncated', 'price_paperback', 'price_hardback', 'image', 'image2', 'image3', 'image4', 'image5', 'image6')

    def description_truncated(self, obj):
        return obj.description[:50]  # Truncate to 50 characters
    description_truncated.short_description = 'Description'  # Column header

    def description2_truncated(self, obj):
        return obj.description2[:50]  # Truncate to 50 characters
    description2_truncated.short_description = 'Description 2'  # Column header

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