from django.urls import path
from .views import all_products,product_details,updateItem,cart,add_product,edit_product

app_name ="products"

urlpatterns = [
    path('shop/', all_products, name='productPage'), 
    path('update_item/', updateItem, name="update_item"),
    path('cart/', cart, name="cart_page"),
    path('product_details/<int:pk>/',product_details , name='product_details'),  

    path('add_product/', add_product, name="add_product_page"),  
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),   
] 