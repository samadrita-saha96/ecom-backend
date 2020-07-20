from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Address, CustomUser,Product
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True,'required': True}}

    def create(self, validated_data):
        newuser = CustomUser.objects.create_user(**validated_data)
        user = CustomUser.objects.filter(email=validated_data.get('email')).values_list()
        uid = (user[0][0])
        url=f"https://elite-in.herokuapp.com/reg/{uid}/"
        subject, from_email, to = 'Verification Email From Elite', settings.EMAIL_HOST_USER, validated_data.get('email')
        text_content = 'Verify Your Email'
        html_content = f"<!DOCTYPE html><html><body><div>Dear {validated_data.get('first_name')},<br> Please verify your email address to complete your Elite Account.<br><a href={url}>Click here</a></div></body></html>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        
        #Token.objects.create(user=newuser)
        return newuser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
