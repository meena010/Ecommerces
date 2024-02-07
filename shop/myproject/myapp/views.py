from django.shortcuts import render, redirect
from .models import * 
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to a success page.
            return redirect('store')
        else:
        # Return an 'invalid login' error message.
            messages.success(request, ("There was a problem logging in, Try again"))
            return redirect('login_user')
    else:
        context={}
    return render(request, 'login.html', context)
    


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create( customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = { 'get_cart_total': 0 , 'get_cart_items':0}
        cartItems = order[ 'get_cart_items' ]
            
    Coffees = Coffee.objects.all()
    context = {'coffees':Coffees, 'cartItems' : cartItems}
    return render(request,"store.html", context )

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create( customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = { 'get_cart_total': 0 , 'get_cart_items':0}
        cartItems = order[ 'get_cart_items' ]

    context = {'items' : items, 'order': order, 'cartItems' : cartItems }
    return render(request,"cart.html", context )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create( customer = customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = { 'get_cart_total': 0 , 'get_cart_items':0}
        cartItems = order[ 'get_cart_items' ]

    context = {'items' : items, 'order': order, 'cartItems' : cartItems}
    return render(request,"checkout.html", context )

def updateItem(request):
    data = json.loads(request.body)
    coffeeId = data['coffeeId']
    action = data['action']
    print('Action:', action)
    print('Coffee:', coffeeId)

    customer = request.user.customer
    coffee = Coffee.objects.get(id = coffeeId)
    order, created = Order.objects.get_or_create(customer = customer, complete= False)

    orderItem, created = OrderItem.objects.get_or_create(order=order , coffee = coffee ) 
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    

    return JsonResponse('Item was added', safe=False)



