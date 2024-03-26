from django.contrib import admin
from .models import Category, Product, Basket, BasketItem, Review, ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'message', 'created_at')  # fields to display in the list view

admin.site.register(ContactMessage, ContactMessageAdmin)  # register ContactMessageAdmin with ContactMessage
admin.site.register(Category)
admin.site.register(Product)
admin.site.site_header = 'Auhtor Commerce Admin Portal'
admin.site.site_title = 'Admin Operations'