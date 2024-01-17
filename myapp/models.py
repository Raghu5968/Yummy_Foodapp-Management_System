
from django.db import models

from django.contrib.auth.models import User
from django import template

register = template.Library()

# Create your models here.
class Foodappusers(models.Model):
    user=models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE,related_name='foodappusers')
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    city=models.CharField(max_length=100,null=True)
    number=models.IntegerField(null=True)
    password=models.CharField(max_length=100)
    profile_pic=models.ImageField(default="pic.png",null=True,blank=True)
    def __str__(self):
        return self.username
    

class Category(models.Model):
    name=models.CharField(max_length=30)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    CATEGORY=(
        ('Starters','Starters'),
        ('BreakFast','BreakFast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner')
    )
    itemname=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    quantity = models.IntegerField(default=1,null=True)
    image=models.ImageField(upload_to='uploads',default='')
    category=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    description=models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.itemname
    
    
    @staticmethod
    def get_all_items():
        return Item.objects.all()
    
    @staticmethod
    def get_all_items_by_categoryid(category_id):
        if category_id:
            return Item.objects.filter(category=category_id)
        else:
            return Item.get_all_items()

    def _str_(self):
        return self.itemname 
    
class Order(models.Model):
    STATUS=(
            ('Pending','Pending'),
            ('Out for delivery','Out for delivery'),
            ('Delivered','Delivered')
        )
    foodappusers=models.ForeignKey(Foodappusers,null=True,on_delete=models.SET_NULL)
    item=models.ManyToManyField(Item)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    quantity = models.IntegerField(default=1,null=True)
    price = models.IntegerField(null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
  
    def _str_(self):
        return self.itemname

class feedback(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    itemname=models.CharField(max_length=100)
    message=models.CharField(max_length=300)
    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='carts')
    
    

class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    items=models.ForeignKey(Item,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.items}"

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1


@register.filter(name='is_in_cart')
def is_in_cart(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(product  , cart):
    return product.price * cart_quantity(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    return sum




class Seller(models.Model):
    name=models.CharField(max_length=100,default='Raghu')
    address=models.TextField(max_length=100,default='Hyderabad')
    email=models.EmailField(max_length=100,default='raghu123@gmail.com')
    number=models.CharField(max_length=150,default='6110787666')
    def __str__(self):
        return self.name