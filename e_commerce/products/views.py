from django.shortcuts import render
from products.models import Product

# Create your views here.
def all_products(request):
    all_products = Product.objects.all()
    return render(request,'products/shop.html',{'all_products':all_products})

def product_details(request,pk):
    object = Product.objects.get(pk=pk)
    return render(request,'products/product_details.html',{'object':object})