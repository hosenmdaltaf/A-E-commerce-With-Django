from orders.models import Order

def cart_context(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        return{
            'cartItems':cartItems
        } 


