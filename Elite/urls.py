from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from rest_framework import routers
from api import views
from django.views.static import serve

router= routers.DefaultRouter()
router.register(r'user',views.CustomUserViewSet)
router.register(r'address',views.AddressViewSet)
#router.register(r'cart',views.CartViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/',views.Customobtain_auth_token),
    path('get_logged_user/',views.LoggedUser),
    path('logout/',views.logoutUser),
    path('reg/<int:uid>/',views.verify),
    path('forget_password/',views.forget_password),
    path('new-password/<str:uid>/',views.newpass),
    path('password-reset-done/',views.passwordResetDone),
    path('productbysub/',views.ProductSubview),
    path('singleproduct/',views.singleProduct.as_view()),
    path('latestproduct/',views.latestproduct.as_view()),
    path('productbyname/',views.ProductByName.as_view()),
    path('cart/',views.addtocart.as_view()),
    path('viewcart/',views.cartview.as_view()),
    path('removecart/',views.cartremove.as_view()),
    path('changequan/',views.changequantity.as_view()),
    path('getUserAddress/',views.GetUserAddress.as_view()),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]