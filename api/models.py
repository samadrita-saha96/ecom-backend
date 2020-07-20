from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from rest_framework.authtoken.models import Token

# Create your models here.

#Custom User Models

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

#User Address Model

class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    country=models.CharField("Country",max_length=50)
    fullname=models.CharField("Full Name",max_length=100)
    mobile=models.CharField("Mobile Number",max_length=10,validators=[MinLengthValidator(10)])
    pin=models.CharField("Pin Code",max_length=6, validators=[MinLengthValidator(6)])
    housenumber=models.CharField("House Number",max_length=90,blank=True)
    street=models.CharField("Street",max_length=80)
    landmark=models.CharField("Landmark",max_length=80,blank=True)
    city=models.CharField("City",max_length=90)
    state=models.CharField("State",max_length=100)
    preferences=models.TextField("Preference")



# Product Table Start

class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"    

    category_name=models.CharField(max_length=70)
    category_image=models.ImageField(upload_to="category-img",blank=True)
    category_description=models.TextField()

    def __str__(self):
        return self.category_name

class Sub_category(models.Model):
    class Meta:
        verbose_name_plural="sub-category"

    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name_plural="Product"
    product_name = models.CharField(max_length=255)
    img1=models.ImageField(upload_to="product_img/img1")
    img2=models.ImageField(upload_to="product_img/img2",blank=True)
    img3=models.ImageField(upload_to="product_img/img3",blank=True)
    price=models.FloatField()
    stock=models.CharField(max_length=3)
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_id=models.ForeignKey(Sub_category,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    
    
class Cart_items(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    product_img=models.CharField(max_length=255)
    product_price=models.FloatField()
    size=models.CharField(max_length=5)
    quantity=models.IntegerField()
    
    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together=(('user','product_name','size'),)