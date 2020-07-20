from django.contrib import admin
from django.contrib.auth.models import User
from .models import CustomUser,Address,Category,Sub_category,Product,Cart_items

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Product)
admin.site.register(Cart_items)