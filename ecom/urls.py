from django.contrib import admin
from django.urls import path,include
from ecom.views import get_products


urlpatterns = [

    path('<slug>/',get_products,name="get_products")
    
    
]