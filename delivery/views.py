from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
import razorpay

from .models import Customer, Restaurant, Item, Cart


# ------------------ BASIC PAGES ------------------
def index(request):
    return render(request, 'delivery/index.html')

def open_signin(request):
    return render(request, 'delivery/signin.html')

def open_signup(request):
    return render(request, 'delivery/signup.html')


# ------------------ AUTH ------------------
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        if not username or not password or not email or not mobile or not address:
            return render(request, 'delivery/fail.html', {'message': 'Please fill all fields.'})

        if Customer.objects.filter(username=username).exists():
            return render(request, 'delivery/fail.html', {'message': 'Username already exists!'})

        Customer.objects.create(username=username, password=password, email=email,
                                mobile=mobile, address=address)

        return render(request, 'delivery/success.html', {
            'message': f'Welcome {username}, your account was created successfully!',
            'next_url': 'index'
        })

    return render(request, 'delivery/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = Customer.objects.get(username=username, password=password)
        except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html', {'message': 'Invalid login!'})

        if username.lower() == "admin":
            return render(request, 'delivery/admin_home.html')

        request.session['username'] = username
        return redirect('customer_home', username=username)

    return redirect('open_signin')


# ------------------ CUSTOMER HOME ------------------
def customer_home(request, username):
    restaurants = Restaurant.objects.all()

    return render(request, 'delivery/customer_home.html', {
        "restaurantList": restaurants,
        "username": username,
        "MEDIA_URL": settings.MEDIA_URL
    })


# ------------------ MENU MANAGEMENT ------------------
def open_update_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = restaurant.items.all()
    return render(request, 'delivery/update_menu.html', {
        "itemList": items,
        "restaurant": restaurant
    })


def view_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)

    return render(request, 'delivery/customer_menu.html', {
        'itemList': items,
        'username': username,
        'restaurant': restaurant,
        'MEDIA_URL': settings.MEDIA_URL
    })


# ------------------ CART ------------------
def add_to_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(Item, id=item_id)

    cart, created = Cart.objects.get_or_create(customer=customer)
    if item not in cart.items.all():
        cart.items.add(item)

    return redirect('show_cart', username=username)


def show_cart(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    items = cart.items.all() if cart else []
    total = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html', {
        "itemList": items,
        "total_price": total,
        "username": username
    })


# ------------------ CHECKOUT ------------------
def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    items = cart.items.all()
    total_price = cart.total_price()

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    order = client.order.create({
        'amount': int(total_price * 100),
        'currency': 'INR',
        'payment_capture': '1',
    })

    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': items,
        'total_price': total_price,
        'order_id': order.get('id'),
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'MEDIA_URL': settings.MEDIA_URL,
    })
