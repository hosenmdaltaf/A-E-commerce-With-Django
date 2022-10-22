from django.shortcuts import render
from products.models import Product

# Create your views here.
def all_products(request):
    all_products = Product.objects.all()
    return render(request,'products/shop.html',{'all_products':all_products})