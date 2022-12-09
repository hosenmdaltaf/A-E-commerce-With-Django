from django.shortcuts import render
from products.models import Product,Category
from .models import Slider
# Create your views here.

def homepage(request):
    all_slider = Slider.objects.all()  
    products = Product.objects.filter(is_verified=True)
    categories = Category.objects.all()  
    context = {
    'all_slider':all_slider,
    'products':products,
    'categories':categories
    }
    return render(request,'homeapp/index.html',context)

def success(request):
 
    return render(request,'homeapp/success.html')