from .models import Cart, CartIteams, Profile
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartIteams)

