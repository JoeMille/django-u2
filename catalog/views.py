# Standard library imports
from django import forms
from django.conf import settings
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse
from .forms import UserUpdateForm, UserProfileForm


# Third party imports
import stripe
from stripe.error import InvalidRequestError

# Local application imports
from .forms import CustomUserCreationForm
from .models import Category, Product, Basket, BasketItem, Review, ContactMessage, Sale, Order, OrderItem, UserProfile

# Index page view
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    # Fetch the basket for the current user
    basket = None
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
    
    # Fetch featured products 
    featured_products = Product.objects.filter(featured=True)[:4]

    return render(request, 'catalog/index.html', {'form': form, 'basket': basket, 'featured_products': featured_products})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            house_number = form.cleaned_data.get('house_number')
            street_name = form.cleaned_data.get('street_name')
            town_city = form.cleaned_data.get('town_city')
            county = form.cleaned_data.get('county')
            eir_code = form.cleaned_data.get('eir_code')
            try:
                UserProfile.objects.create(user=user, house_number=house_number, street_name=street_name, town_city=town_city, county=county, eir_code=eir_code)
            except IntegrityError as e:
                print(e)
                return render(request, 'catalog/register.html', {'form': form, 'error': 'Failed to create user profile.'})
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})

# Logout view

def logout(request):
    auth_logout(request)
    return redirect('index')

# About page view
def about(request):
    return render(request, 'catalog/about.html')

# Products page view
def products(request):
    categories = Category.objects.prefetch_related(
        Prefetch('product_set', queryset=Product.objects.all().order_by('id'), to_attr='products')
    )
    return render(request, 'catalog/products.html', {'categories': categories})

# Product_detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})

# Checkout page view
def checkout(request):
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
        for item in basket.basketitem_set.all():
            print(item.product.title)  # Print the title of the product
        return render(request, 'catalog/checkout.html', {'basket': basket})
    else:
        return redirect('login')

class AddToBasketForm(forms.Form):
    book_type = forms.ChoiceField(choices=Product.BOOK_TYPES)


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket = Basket.objects.get(user=request.user)

    print(f"User: {request.user}")  # Debug: print the user
    print(f"Product: {product}")  # Debug: print the product

    if request.method == 'POST':
        form = AddToBasketForm(request.POST)

        if form.is_valid():
            book_type = form.cleaned_data.get('book_type')

            if book_type == 'PB':
                price = product.price_paperback
            elif book_type == 'HB':
                price = product.price_hardback
            else:
                price = 0.00  # default price

            basket_item, created = BasketItem.objects.get_or_create(
                product=product,
                basket=basket,
            )

            basket_item.price = price
            basket_item.save()

            print(f"Basket item: {basket_item}")  # Debug: print the basket item

    return redirect('products')

# Remove items from checkout basket 
def remove_from_basket(request, item_id):
    if request.method == 'POST':
        item = BasketItem.objects.get(id=item_id)
        item.delete()
    return redirect('checkout')

# Payment page view
def payment(request):
    return render(request, 'catalog/payment.html')
    
# Stripe payment view
@csrf_exempt
def charge(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']

        # Get the user's basket
        basket = Basket.objects.filter(user=request.user).first()
        if not basket:
            return HttpResponse('No items in basket', status=400)

        # Calculate the total cost of the items in the basket
        total_cost = 0
        for item in basket.basketitem_set.all():
            total_cost += item.product.price * item.quantity

        # Convert total_cost to pence (or the smallest currency unit)
        total_cost = int(total_cost * 100)

        # Create Stripe charge
        try:
            charge =  stripe.Charge.create(
                amount=int(total_cost * 100),  # Convert total cost to cents
                currency='eur',  # Use euros
                description='Example charge',
                source=token,
            )
        except InvalidRequestError as e:
            return HttpResponse(f'Error: {str(e)}', status=400)

        # Create Order object
        try:
            order = Order.objects.create(
                user=request.user,
                total_cost=total_cost/100,  # Add the total cost here
                # Add other necessary fields here
            )

            # Create OrderItem objects for each item in the basket
            for item in basket.basketitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    # Add other necessary fields here
                )

            # Clear the basket
            basket.basketitem_set.all().delete()

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=400)

        # Redirect to a "payment complete" page after a successful charge
        return redirect('charge')

    return render(request, 'catalog/charge.html')

def create_order_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending', defaults={'total_cost': 0})
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 1})
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('charge') 

# Reviews page view
def reviews(request):
    reviews = Review.objects.all()  
    products = Product.objects.all() 
    print(reviews) # Print all reviews to the terminal test REMOVE THIS LINE 
    return render(request, 'catalog/reviews.html', {'reviews': reviews, 'products': products})

def create_review(request):
    products = Product.objects.all()  
    print(products) # Print all products to the terminal test REMOVE THIS LINE
    if request.method == 'POST':
        review = Review()
        review.user = request.user
        review.product = Product.objects.get(pk=request.POST['product_id'])
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return redirect('reviews')
    return render(request, 'catalog/create_review.html', {'products': products})

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        if request.user == review.user:
            review.rating = request.POST['rating']
            review.comment = request.POST['comment']
            review.save()
        return redirect('reviews')
    else:
        if request.user != review.user:
            return redirect('reviews')
        return render(request, 'catalog/edit_review.html', {'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('reviews')

def dashboard(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'catalog/dashboard.html', {'user_form': user_form, 'profile_form': profile_form})