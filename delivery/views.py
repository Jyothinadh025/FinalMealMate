from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import razorpay
from razorpay.errors import BadRequestError, SignatureVerificationError

from .models import Customer, Restaurant, Item, Cart


# ------------------ BASIC PAGES ------------------
def index(request):
    return render(request, 'delivery/index.html')


def open_signin(request):
    return render(request, 'delivery/signin.html')


def open_signup(request):
    return render(request, 'delivery/signup.html')


# ------------------ AUTHENTICATION ------------------
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        if not username or not password or not email or not mobile or not address:
            return render(request, 'delivery/fail.html', {'message': 'Please fill in all required fields.'})

        if Customer.objects.filter(username=username).exists():
            return render(request, 'delivery/fail.html', {'message': 'Username already exists!'})

        Customer.objects.create(username=username, password=password, email=email, mobile=mobile, address=address)
        return render(request, 'delivery/success.html', {
            'message': f'Welcome to Meal Buddy, {username}! Your account has been created successfully.',
            'next_url': 'index'
        })
    return render(request, 'delivery/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'delivery/fail.html', {'message': 'Please enter both username and password.'})

        try:
            user = Customer.objects.get(username=username, password=password)
        except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html', {'message': 'Invalid username or password.'})

        if username.lower() == 'admin':
            return render(request, 'delivery/admin_home.html')

        request.session['username'] = username
        return render(request, 'delivery/success.html', {
            'message': f'Welcome back, {username}!',
            'next_url': 'customer_home',
            'username': username
        })
    return redirect('open_signin')


# ------------------ CUSTOMER HOME ------------------
def customer_home(request, username):
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/customer_home.html', {"restaurantList": restaurantList, "username": username})


# ------------------ RESTAURANT MANAGEMENT ------------------
def open_add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html')


def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        picture = request.POST.get('picture', '').strip()
        cuisine = request.POST.get('cuisine', '').strip()
        rating = request.POST.get('rating', '').strip()

        if not name or not cuisine or not rating:
            return render(request, 'delivery/fail.html', {'message': 'Please fill in all restaurant details.'})

        if Restaurant.objects.filter(name=name).exists():
            return render(request, 'delivery/fail.html', {'message': 'Restaurant already exists!'})

        Restaurant.objects.create(name=name, picture=picture, cuisine=cuisine, rating=rating)
        return render(request, 'delivery/success.html', {'message': f'Restaurant "{name}" added!', 'next_url': 'open_show_restaurant'})
    return render(request, 'delivery/add_restaurant.html')


def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurantList": restaurantList})


def open_update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/update_restaurant.html', {"restaurant": restaurant})


def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        restaurant.name = request.POST.get('name', restaurant.name)
        restaurant.picture = request.POST.get('picture', restaurant.picture)
        restaurant.cuisine = request.POST.get('cuisine', restaurant.cuisine)
        restaurant.rating = request.POST.get('rating', restaurant.rating)
        restaurant.save()
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurantList": restaurantList})


def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurantList": restaurantList})


# ------------------ MENU MANAGEMENT ------------------
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    itemList = restaurant.items.all()
    return render(request, 'delivery/update_menu.html', {"itemList": itemList, "restaurant": restaurant})


def update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')

        if Item.objects.filter(name=name, restaurant=restaurant).exists():
            return render(request, 'delivery/fail.html', {'message': 'Item already exists for this restaurant.'})

        Item.objects.create(restaurant=restaurant, name=name, description=description, price=price, vegeterian=vegeterian, picture=picture)
    return render(request, 'delivery/admin_home.html')


# ------------------ CUSTOMER MENU VIEW ------------------
def view_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)
    return render(request, 'delivery/customer_menu.html', {'itemList': items, 'username': username})


# ------------------ CART OPERATIONS ------------------
def add_to_cart(request, item_id, username):
    item = get_object_or_404(Item, id=item_id)
    customer = get_object_or_404(Customer, username=username)
    cart, created = Cart.objects.get_or_create(customer=customer)
    # avoid duplicates
    if item not in cart.items.all():
        cart.items.add(item)
    return redirect('show_cart', username=username)


def show_cart(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    return render(request, 'delivery/cart.html', {"itemList": items, "total_price": total_price, "username": username})


# ------------------ CHECKOUT (RAZORPAY) ------------------
def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if not cart_items or total_price <= 0:
        return render(request, 'delivery/checkout.html', {
            'username': username,
            'cart_items': [],
            'total_price': 0,
            'error': 'Your cart is empty!'
        })

    # create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_data = {
        'amount': int(total_price * 100),
        'currency': 'INR',
        'payment_capture': '1',
    }

    try:
        order = client.order.create(data=order_data)
    except BadRequestError as e:
        # Could be authentication failed or other issue
        return render(request, 'delivery/fail.html', {'message': f'Razorpay error: {str(e)}'})

    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order.get('id'),
        'amount': total_price,
    })


# ------------------ ORDERS (SUCCESS) ------------------
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    if cart:
        cart.items.clear()
    return render(request, 'delivery/success.html', {
        'message': f'Thank you, {username}! Your payment and order were successful.',
        'next_url': 'index'
    })


# ------------------ FAIL PAGE ------------------
def fail_page(request):
    return render(request, 'delivery/fail.html', {'message': 'Something went wrong. Please try again.'})
