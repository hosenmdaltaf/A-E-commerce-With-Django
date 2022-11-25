from django.shortcuts import render
from products.models import Product
from .models import Slider
# Create your views here.

def homepage(request):
    all_slider = Slider.objects.all()  
    products = Product.objects.all() 
    context = {
    'all_slider':all_slider,
    'products':products
    }
    return render(request,'homeapp/index.html',context)