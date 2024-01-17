from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(Foodappusers)

admin.site.register(Item)

admin.site.register(Order)

admin.site.register(Category)

admin.site.register(Cart)

admin.site.register(CartItems)

admin.site.register(Seller)


