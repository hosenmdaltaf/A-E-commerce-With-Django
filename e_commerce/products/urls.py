from django.urls import path
from .views import all_products

app_name ="products"

urlpatterns = [
    path('', all_products, name='productPage'),    
] 