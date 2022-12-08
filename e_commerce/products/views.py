from django.shortcuts import render,redirect, get_object_or_404
from products.models import Product
from orders.models import Order,OrderItem
from users.models import Accounts
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

# Create your views here.
def all_products(request):  
    all_products = Product.objects.filter(is_verified=True)
    context = {
    'all_products':all_products,
    }
    return render(request,'products/shop.html',context)

def product_details(request,pk):
    object = Product.objects.get(pk=pk)
    related_products = Product.objects.filter(is_verified=True)
    return render(request,'products/product_details.html',{'related_products':related_products,'object':object})

from django.http import JsonResponse
import json

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId'] 
	action = data['action']
	customer = request.user
    # customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
	if action == 'add': 
		orderItem.quantity = (orderItem.quantity + 1)  
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	# elif action == 'delete':
	# 	orderItem.remove()
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		products =Product.objects.filter(is_verified=True)[:5]
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
        
	context = {
    'items':items, 
    'order':order,
    'cartItems':cartItems,
    'products':products,
     }
	return render(request, 'orders/cart.html', context) 
	#return render(request, 'orders/newCart.html', context) 


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
    
            print(form)
            return redirect('users:profilePage')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    vendor = request.user
    product = vendor.products.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('users:profilePage')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {'form': form,'product': product})

   
