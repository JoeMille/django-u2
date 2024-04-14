from django import forms
from django.contrib import admin
from .models import Category, Product, Basket, BasketItem, Review, ContactMessage, Order, OrderItem

class ProductAdminForm(forms.ModelForm):
    description2 = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['title', 'category', 'image', 'description', 'price', 'short_description2', 'image2', 'image3', 'image4']

    def short_description2(self, obj):
        return obj.description2[:50]  # Truncate to 50 characters
    short_description2.short_description = 'Description 2'  # Column header

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # this is the number of extra forms displayed

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_type', 'total_cost', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)  # register OrderAdmin with Order
admin.site.register(ContactMessage)  # register ContactMessage without a custom admin
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # register ProductAdmin with Product
admin.site.site_header = 'Penny Miller Books Administration'
admin.site.site_title = 'Admin Operations'