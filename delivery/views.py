from django.shortcuts import render, redirect
from .models import Customer, Restaurant, Item, Cart, CartItem
import razorpay
from meal_buddy.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# -------------------------------------------
# INDEX / SIGNIN / SIGNUP
# -------------------------------------------
def index(request):
    return render(request, 'delivery/index.html')


def open_signin(request):
    return render(request, 'delivery/signin.html')


def open_signup(request):
    return render(request, 'delivery/signup.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']

        if Customer.objects.filter(username=username).exists():
            return render(request, 'delivery/fail.html', {"message": "Username already exists!"})

        Customer.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        return redirect('open_signin')

    return redirect('open_signup')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Customer.objects.get(username=username, password=password)
        except:
            return render(request, 'delivery/fail.html', {"message": "Invalid login details"})

        return redirect('customer_home', username=user.username)

    return redirect('open_signin')


# -------------------------------------------
# USER HOME + MENU
# -------------------------------------------
def customer_home(request, username):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/customer_home.html', {
        "username": username,
        "restaurantList": restaurants
    })


def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    items = Item.objects.filter(restaurant=restaurant)

    return render(request, 'delivery/customer_menu.html', {
        "username": username,
        "restaurant": restaurant,
        "itemList": items
    })


# -------------------------------------------
# CART FUNCTIONS (+ / - / REMOVE)
# -------------------------------------------
# ---------------- ADD TO CART ----------------
def add_to_cart(request, item_id, username):
    customer = Customer.objects.get(username=username)
    cart, created = Cart.objects.get_or_create(customer=customer)
    item = Item.objects.get(id=item_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    # If item is already in cart, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('show_cart', username=username)


# ---------------- SHOW CART ----------------
def show_cart(request, username):
    customer = Customer.objects.get(username=username)
    cart, created = Cart.objects.get_or_create(customer=customer)

    cart_items = CartItem.objects.filter(cart=cart)
    total = cart.total_price()

    return render(request, 'delivery/cart.html', {
        "username": username,
        "cart_items": cart_items,
        "total_price": total
    })


# ---------------- INCREASE ----------------
# ---------------- INCREASE ----------------
def increase_quantity(request, cart_item_id, username):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart', username=username)

# ---------------- DECREASE ----------------
def decrease_quantity(request, cart_item_id, username):
    cart_item = CartItem.objects.get(id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('show_cart', username=username)

# -------------------------------------------
# RAZORPAY CHECKOUT
# -------------------------------------------
def checkout(request, username):
    customer = Customer.objects.get(username=username)
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = cart.total_price()

    if total_price <= 0:
        return render(request, 'delivery/fail.html', {"message": "Your cart is empty!"})

    total_price_in_paise = int(total_price * 100)

    # Create Razorpay client
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order = client.order.create({
        "amount": total_price_in_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, 'delivery/checkout.html', {
        "username": username,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_price_in_paise": total_price_in_paise,
        "order_id": order["id"],
        "razorpay_key_id": RAZORPAY_KEY_ID,
    })


# -------------------------------------------
# ORDER SUCCESS PAGE
# -------------------------------------------
def order_success(request, username):
    customer = Customer.objects.get(username=username)

    return render(request, "delivery/orders.html", {
        "username": username,
        "customer": customer
    })
