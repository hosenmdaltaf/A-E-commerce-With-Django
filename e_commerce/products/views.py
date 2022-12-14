from django.shortcuts import render,redirect, get_object_or_404
from products.models import Product,Category
from orders.models import Order,OrderItem,ShippingAddress
from users.models import Accounts
from django.contrib.auth.decorators import login_required
from .forms import ProductForm 
from django.contrib import messages

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

@login_required(login_url='users:loginPage')
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

@login_required(login_url='users:loginPage')
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

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if request.method == "POST":
            try:
                address = request.POST.get("address")
                city = request.POST.get("city")
                state = request.POST.get("state")
                zipcode = request.POST.get("zipcode") 
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    )
                return render(request,'homeapp/success.html')
            except:
                messages.warning(request, 'Please fill up all the form feild currectly!')
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'orders/checkout.html', context)


def category(request, pk): 
    # category = get_object_or_404(Category, pk=pk)
    category = Product.objects.filter(category=pk).filter(is_verified=True)
    return render(request, 'products/category.html', {'category': category}) 


@login_required(login_url='users:loginPage')
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

@login_required(login_url='users:loginPage')
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

   
