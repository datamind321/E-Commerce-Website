from django.contrib import admin
from django.urls import path,include
from account.views import activate_email, cart, login_page, register_page,add_to_cart, remove_cart, remove_coupan
# from ecom.views import add_to_cart



urlpatterns = [
    path('login/',login_page,name="login"),
    path('register/',register_page,name="register"),
    path('activate/<email_token>/',activate_email,name="activate_email"),
    path('cart/',cart,name="cart"),
    path('add-to-cart/<uid>/',add_to_cart,name="add_to_cart"),
    path('remove-cart/<cart_item_uid>/',remove_cart,name="remove_cart"),
    path('remove-coupan/<cart_id>/',remove_coupan,name="remove_coupan")

]