from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .serializers import CustomUserSerializer,AddressSerializer,ProductSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets,status
from .models import Address,CustomUser,Product,Sub_category,Cart_items
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .encrypt_decrypt import encrypt,decrypt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=(AllowAny,)

#Custom Obtain Auth Token

class AuthToken(APIView):
    def post(self, request):
        data=request.data
        print(data.get('password'))
        Context={
            'error':"Invalid Email"
        }
        if CustomUser.objects.filter(email=data.get('email')).exists():
            id1=CustomUser.objects.get(email=data.get('email'))
            user=CustomUser.objects.get(id=id1.id)
            match_pass=check_password(data.get('password'),user.password)
        
            if match_pass:
                token=Token.objects.get(user_id=id1)
                login(request,user)
                Context={
                    'token':token.key,
                    'id':token.user_id
                }
                return Response(Context)
            else:
                Context={
                    'error':'Invalid Password!'
                }
                return Response(Context,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(Context,status=status.HTTP_404_NOT_FOUND)
Customobtain_auth_token=AuthToken.as_view()

#Logout User
@csrf_exempt
def logoutUser(request):
    print(request.user)
    logout(request)
    return HttpResponse("Logout")

#Get Logged in User
class LoggedInUser(APIView):
    def post(self,request):
        data=request.data
        id1=Token.objects.get(key=data.get('token'))
        user=CustomUser.objects.get(id=id1.user_id)
        Context={
            'id':user.id,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
        
        }
        return Response(Context)
LoggedUser=LoggedInUser.as_view()

class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
    permission_classes=(AllowAny,)

def verify(request,uid):
    newuser=CustomUser.objects.get(id=uid)
        
    Token.objects.create(user=newuser)
    return render(request,'verify.html')


class forgetpassword(APIView):
    #permission_classes = (IsAdminUser,)

    def post(self,request):
        data=request.data
        eml=(data.get('email'))
        uid=encrypt(CustomUser.objects.filter(email=eml).values_list()[0][0])
        url=f"https://elite-in.herokuapp.com/new-password/{uid}"

        text_content="Hello"
        subject, from_email, to = 'Elite Password Reset', settings.EMAIL_HOST_USER, data.get('email')
        html_content = f"<!DOCTYPE html><html><body><div>We have just received a password reset request for {data.get('email')} <br>Please <a href={url}>Click here</a> to reset your password.<br><br>Thank You<br>Team Elite</div></body></html>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return Response("Mail Sent")
forget_password=forgetpassword.as_view()


def newpass(request,uid):
    id1=(decrypt(uid))
    #print(id1)
    if CustomUser.objects.filter(id=id1).exists():
        return render(request,'forget_pass.html',{'uid':id1})
    else:
        return HttpResponse(status=404) 
  
@csrf_exempt   
def passwordResetDone(request):
    id1=(request.POST['id_u'])
    user=CustomUser.objects.get(id=id1)
    user.set_password(request.POST['np'])
    user.save()
    return render(request,'passwordResetDone.html')


#Product Viewsets
class Productsub(APIView):
    def post(self,request):
        subid=request.data.get('subid')
        datas=list(Product.objects.filter(sub_id_id=subid).values())
        return JsonResponse(datas,safe=False)
ProductSubview=Productsub.as_view()

class singleProduct(APIView):
    def post(self,request):
        pid=request.data.get('pid')
        qset=list(Product.objects.filter(id=pid).values())
        return JsonResponse(qset,safe=False)

class latestproduct(APIView):
    def get(self,request):
        qset=list(Product.objects.all().values())
        qset.reverse()
        return JsonResponse(qset[:8],safe=False)

class ProductByName(APIView):
    def post(self,request):
        pname=request.data.get('pname')
        pname=(pname.replace('_',' '))
        print(pname)
        qset=list(Product.objects.filter(product_name=pname).values())
        if qset:
            return JsonResponse(qset,safe=False)
        else:
            return Response("Not Found")

# class CartViewSet(viewsets.ModelViewSet):
#     queryset=Cart_item.objects.all()
#     serializer_class=CartSerializer
#     #permission_classes=(IsAdminUser,)

class addtocart(APIView):
    def post(self,request):
        prod=Product.objects.get(product_name=request.data.get('product_name'))
        user=CustomUser.objects.get(email=request.data.get('user'))
        qset=(Cart_items.objects.all())
        print((qset))
        flag=0
        for q in qset:
            if q.user==user and str(q.product_name)==str(prod) and q.size==request.data.get('size'):
                q.quantity+=1
                q.save()
                flag=1
                break
            else:
                flag=0
        if flag==0:
            quan=request.data.get('quantity')
            sz=request.data.get('size')
            price=request.data.get('price')
            img=request.data.get('img')
            Cart_items.objects.create(user=user,product_name=prod,size=sz,quantity=quan,product_price=price,product_img=img)
        return Response("Done")

class cartview(APIView):
    def post(self,request):
        uemail=request.data.get('uemail')
        uid=CustomUser.objects.get(email=uemail)
        items=list(Cart_items.objects.filter(user_id=uid).values())
        
        return JsonResponse(items,safe=False) 

class cartremove(APIView):
    def post(self,request):
        cart_id=request.data.get('cartid')
        items=Cart_items.objects.filter(id=cart_id).delete()
        # print(items)
        return Response("Done")

class changequantity(APIView):
    def post(self,request):
        cart_id=request.data.get('cartid')
        quan=request.data.get('quantity')
        qset=Cart_items.objects.get(id=cart_id)
        qset.quantity=quan
        qset.save()
        return Response("Done")


class GetUserAddress(APIView):
    def post(self,request):
        qs=list(Address.objects.filter(user=request.data.get('uid')).values())
        qs.reverse()
        return JsonResponse(qs,safe=False)