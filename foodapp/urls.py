"""
URL configuration for foodapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
# from django.conf.urls import url 

from myapp import views
from django.conf import settings

from django.conf.urls.static import static

app_name='loadmap' 

urlpatterns = [
    path('',views.home,name="home"),
    path("about",views.about,name="about"),
    path("menu",views.menu,name="menu"),
    path("contact",views.contact,name="contact"),
    path("orders",views.orders,name="orders"),
    path("settings",views.settings,name="settings"),
    path("registerpage/",views.registerpage,name="registerpage"),
    path("loginpage/",views.loginpage,name="loginpage"),
    path("logoutpage",views.logoutpage,name="logoutpage"),
    
    path("order_form",views.order_form,name="order_form"),
    

    path("items",views.items,name="items"),
    path("admin_dashboard",views.admin_dashboard,name="admin_dashboard"),
    path("customer/<int:pk>",views.customer,name='customer'),
    path('updateOrder/<int:pk>/',views.updateOrder,name="updateOrder"),
    path("admin_profilepage",views.admin_profilepage,name="admin_profilepage"),
    path("createOrder/<str:pk>",views.createOrder,name='createOrder'),
    path("add_to_cart/<str:item_id>",views.add_to_cart,name="add_to_cart"),
    path("remove_from_cart/<str:items_id>",views.remove_from_cart,name="remove_from_cart"),
    path("cartpage",views.cartpage,name="cartpage"),
    path("Feedback",views.Feedback,name="Feedback"),
    path("checkout",views.checkout,name="checkout"),
    path("admin_contact",views.admin_contact,name="admin_contact"),
    path("pdf",views.pdf,name="pdf"),
    path("myorders",views.myorders,name="myorders"),
    path("increment_cart_item/<int:cart_item_id>",views.increment_cart_item,name="increment_cart_item"),
    path("decrement_cart_item/<int:cart_item_id>",views.decrement_cart_item,name="decrement_cart_item"),
    path("userorders/<int:pk>",views.userorders,name="userorders"),
   
    path('admin/', admin.site.urls),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)