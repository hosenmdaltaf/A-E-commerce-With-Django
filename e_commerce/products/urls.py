from django.urls import path
from .views import all_products,product_details

app_name ="products"

urlpatterns = [
    path('', all_products, name='productPage'), 
    path('product_details/<int:pk>/',product_details , name='product_details'),       
] 