from django.shortcuts import render
from products.models import Product
from orders.models import Order,OrderItem
from users.models import Accounts

# Create your views here.
def all_products(request):
    all_products = Product.objects.all() 
    # if request.user.is_authenticated:
    #     customer = request.user
    #     print('Customer name')
    #     print(customer)
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     print('order details')
    #     print(order)
    #     items = order.orderitem_set.all()
    #     print('items details')
    #     print(items)
    #     cartItems = order.get_cart_items
    #     print('cart items')
    #     print(cartItems)
    # else:
	# 	#Create empty cart for now for non-logged in user
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    #     cartItems = order['get_cart_items']

    context = {
    # 'items':items, 
    # 'order':order, 
    'all_products':all_products,
    # 'cartItems':cartItems
    }
    return render(request,'products/shop.html',context)

def product_details(request,pk):
    object = Product.objects.get(pk=pk)
    return render(request,'products/product_details.html',{'object':object})

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
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'orders/cart.html', context) 