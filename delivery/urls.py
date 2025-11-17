from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('open_signin/', views.open_signin, name='open_signin'),
    path('open_signup/', views.open_signup, name='open_signup'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),

    path('customer_home/<str:username>/', views.customer_home, name='customer_home'),
    path('view_menu/<int:restaurant_id>/<str:username>/', views.view_menu, name='view_menu'),

    # CART
    path('add_to_cart/<int:item_id>/<str:username>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<str:username>/', views.show_cart, name='show_cart'),

    # FIXED: must match cartitem_id
   path('increase/<int:cart_item_id>/<str:username>/', views.increase_quantity, name='increase_quantity'),
   path('decrease/<int:cart_item_id>/<str:username>/', views.decrease_quantity, name='decrease_quantity'),

    # PAYMENT
    path('checkout/<str:username>/', views.checkout, name='checkout'),

    # ORDER SUCCESS PAGE
    path('order_success/<str:username>/', views.order_success, name='order_success'),
]
