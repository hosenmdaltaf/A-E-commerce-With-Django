from django.urls import path
from .views import all_products,product_details,updateItem,cart

app_name ="products"

urlpatterns = [
    path('', all_products, name='productPage'), 
    path('update_item/', updateItem, name="update_item"),
    path('cart/', cart, name="cart_page"),
    path('product_details/<int:pk>/',product_details , name='product_details'),       
] 