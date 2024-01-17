from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.models import User,auth

from django.contrib import messages

from .forms import *

from .models import *

from django.http import HttpResponseForbidden

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.forms import inlineformset_factory
import razorpay




# Create your views here.
def home(request):
    form=foodappform
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def menu(request):
    items=Item.get_all_items()
    categories=Category.get_all_categories()
    print(categories)
    categoryID=request.GET.get('category')
    print(categoryID)
    if categoryID:
        items=Item.get_all_items_by_categoryid(categoryID)
    else:
        items=Item.get_all_items()
    data={}
    data['items']=items
    data['categories']=categories
    return render(request,'menu.html',data)


def contact(request):
    return render(request,'contact.html')
#landing page after login
@login_required(login_url='login')


def orders(request):
    orders=Order.objects.all()
    total_Orders=orders.count()
    context={'total_Orders':total_Orders}
    return render(request,'orders.html',context)
@unauthenticated_user
def registerpage(request):
    if request.user.is_authenticated:
        return redirect('orders')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username=form.cleaned_data.get('username')
                group=Group.objects.get(name='customer')
                user.groups.add(group)
                Foodappusers.objects.create(user=user,username=user.username,email=user.email)
                messages.success(request,'User Successfully created for '+username)
                return redirect('registerpage')
    context={'form':form}        
    return render(request,'registration.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('orders') 
        else:
            messages.info(request,'username or password error')
            print("username or password error ")
            return redirect('loginpage')
    return render(request,'login.html')

#after admin login
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def admin_dashboard(request):
        orders=Order.objects.all()
        print(orders)
        # orders = Order.objects.prefetch_related('item').all()
        foodappusers=Foodappusers.objects.all()
        total_foodappuser=foodappusers.count()
        total_orders=orders.count()
        delivered=orders.filter(status='Delivered').count()
        pending=orders.filter(status='Pending').count()
        
        if request.method=='POST':
            status=request.POST['status']
            print(status)
            order_id=request.POST['order_id']
            print(order_id)
            order_to_update = Order.objects.get(id=order_id)
            order_to_update.status=status
            order_to_update.save()
        context={'orders':orders,'foodappusers':foodappusers,'total_orders':total_orders,
             'total_foodappuser':total_foodappuser,'delivered':delivered,'pending':pending} 
        return render(request,'admin_dashboard.html',context)



#products information
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def items(request):
    items=Item.objects.all()
    return render(request,'items.html',{'items':items})

#customer information
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def customer(request,pk):
    customer=Foodappusers.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    context={'customer':customer,'orders':orders,'order_count':order_count,
             }
    
    return render(request,'customer.html',context)


# Create order
def createOrder(request):
    form=Orderform(request.POST)
    customer=Foodappusers.objects.filter(user=request.user)
    if request.method=='POST':
        print(request.POST)
        formset=Orderform(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('checkout')
    context={'form':form}
    return render(request,'order_form.html',context)
def order_form(request):
    return render(request,'order_form.html')


#update order  notusing
def updateOrder(request,pk):
    order=get_object_or_404(Order,id=pk)  
    if request.method=='POST':
        form=Orderform(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard',pk=order.pk)
    else:
        form=Orderform(instance=order)
    context={'form':form,'order':order}   
    return render(request,'updateOrder.html',context)


def logoutpage(request):
    logout(request)
    return redirect('/')

# def userpage(request):
#     orders=request.user.customer.order_set.all()
#     total_orders=orders.count()
#     delivered=orders.filter(status='Delivered').count()
#     pending=orders.filter(status='Pending').count()
#     context={'orders':orders,'total_orders':total_orders,
#              'delivered':delivered,'pending':pending}
   
#     return render(request,'user.html',context)

#user settings
@login_required(login_url='login')

def settings(request):
    foodapps=request.user.foodappusers
    form=foodappform(instance=foodapps)
    if request.method=='POST':
        form=foodappform(request.POST,request.FILES,instance=foodapps)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'settings.html',context)

@login_required(login_url='login')
def admin_profilepage(request):
    return render(request,'admin_profilepage.html')

# @login_required(login_url='login')
# def cartpage(request):
#     return render(request,'cartpage.html')
    


def Feedback(request):
    if request.method == 'POST':
        form = feedbackform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = feedbackform()

    return render(request, 'feedback.html', {'form': form})

@login_required(login_url='login')
def admin_contact(request):
    return render(request,'admin_contact.html')

@login_required(login_url='login')

def add_to_cart (request, item_id):
    items=Item.objects.get(id=item_id)
    user=request.user
    cart ,_=Cart.objects.get_or_create(user=user)
    cart_items=CartItems.objects.create(cart=cart,items=items)
    cart_items.save()
    return redirect('menu')
    
@login_required(login_url='login')

def cartpage(request):
    items=Item.objects.all()
    user=request.user
    cart_items=CartItems.objects.all()
    user_cart=Cart.objects.get_or_create(user=user)[0]
    cart_items=CartItems.objects.filter(cart=user_cart)
    for item in cart_items:
        item.total_price = item.items.price * item.quantity
        item.save()

    total_price = sum(item.quantity * item.items.price for item in cart_items)

    
    context={'items': items, 'cart_items':cart_items,"total_price":total_price,'cart_items':cart_items}
    return render(request,"cartpage.html",context)

@login_required(login_url='login')

def remove_from_cart(request, items_id):
    items = CartItems.objects.get(id=items_id)
    items.delete()
    return redirect('cartpage')

@login_required(login_url='login')

def view_cart(request):
    user = request.user
    user_cart = Cart.objects.get_or_create(user=user)[0]
    
    cart_items = CartItems.objects.filter(cart=user_cart)  
    return render(request, 'cartpage.html', {'cart_items': cart_items})

@login_required(login_url='login')

def checkout(request):
    razor_pay_key_id="rzp_test_d1KQnZuCgGnn9z"
    key_secret="tE89qLKPx8k3iUkhrlHjqiRF"
    cart,_=Cart.objects.get_or_create(user=request.user)
    cart_items=CartItems.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.items.price for item in cart_items)
    client=razorpay.Client(auth=(razor_pay_key_id,key_secret))
    amount=(total_price*100)
    payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
    print(payment)
    user=request.user
    foodappusers=Foodappusers.objects.filter(user=user)
    orders=Order.objects.all()
    total_orders=orders.count()
    for item in cart_items:
        item.total_price = item.items.price * item.quantity
        item.save()
    context={'total_orders':total_orders, 'foodappusers':foodappusers,
             'payment':payment,'cart_items':cart_items,
             "total_price":total_price,'cart_items':cart_items}
    return render(request,'checkout.html',context)



@login_required(login_url='login')
def pdf(request):
    user=request.user
    foodappusers=Foodappusers.objects.filter(user=user)
    seller=Seller.objects.all()
    cart = Cart.objects.get(user=request.user)
    cart_items=CartItems.objects.filter(cart=cart)
    total_price = sum(item.items.price * item.quantity for item in cart_items)
    print(cart)
    print(total_price)
        # Create an order
    order = Order.objects.create(
        user=request.user,
        total_amount=total_price,
        status="Pending"
    )
    
    for item in cart_items:
        item.total_amount = item.items.price * item.quantity
        item.save()
    print(cart_items)
    
    context={'order':order,'foodappusers':foodappusers,'seller':seller}
    return render(request,'pdf.html',context)


@login_required(login_url='login')
def myorders(request):
    user = request.user
    user_cart,_ = Cart.objects.get_or_create(user=request.user)
    foodappusers=Foodappusers.objects.all()
    cart_items = CartItems.objects.filter(cart=user_cart)  
    items=Item.objects.all()
    orders=Order.objects.filter(user=request.user)
    order_count=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    print(cart_items)

    context={'order_count':order_count,'items':items,'foodappusers':foodappusers,'orders':orders,
             'delivered':delivered,'pending':pending,'cart_items': cart_items}
    return render(request,'myorders.html',context)

    # myorder=Foodappusers.objects.get(id=pk)
    
    # orders=myorder.order_set.all()
    # order_count=orders.count()
    # context={'myorder':myorder,'orders':orders,'order_count':order_count,
    #          }
    
    # return render(request,'myorders.html',context)


@login_required(login_url='login')

def increment_cart_item(request,cart_item_id):
    cart_item=get_object_or_404(CartItems, id=cart_item_id)
    cart_item.quantity+=1
    print(cart_item)
    cart_item.save()
    return redirect('cartpage')

@login_required(login_url='login')

def decrement_cart_item(request, cart_item_id):
    cart_item=get_object_or_404(CartItems, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartpage')

@login_required(login_url='login')
def userorders(request,):
    return render(request,'myorders.html')
    

    