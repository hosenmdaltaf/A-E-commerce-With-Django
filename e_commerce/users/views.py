
from django.http import HttpResponse
from users.models import Accounts
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout

from django.views.generic import View
from orders.models import Order,OrderItem
from django.contrib.auth.decorators import login_required

def RegisterView(request):
    ''' Sign up new user to E-commerce '''
    if request.method == 'POST':

        email = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        mobile_number= request.POST.get('mobilenumber')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('confirmpassword') 


        if not (email and password and repeatPassword and last_name and mobile_number and first_name):
            messages.error(request, 'Please fillup all field correctly!!')
            return redirect('users:registerPage')

        if Accounts.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists.')
            return redirect('users:registerPage')

        if Accounts.objects.filter(mobile_number=mobile_number).exists():
            messages.info(request, 'Mobile number already exists.')
            return redirect('users:registerPage')

        if password and repeatPassword:
            if password != repeatPassword:
                messages.warning(request, "The two password fields didn't match.")
                return redirect('users:registerPage')

        user = Accounts.objects.create_user( 
            email=email,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Your Account Is Successfully Created")
         #Successfully registered. Redirect to homepage
        return redirect('users:loginPage')
    return render(request, 'users/register.html')

def LogInView(request):
    ''' Sign in views '''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Accounts.objects.filter(email=email).first() 
        if user is None:
            messages.warning(request, '%s Not found!' % email) 
            return redirect('users:loginPage')

        if not (email and password):
            messages.error(request, 'Please provide all the details!!')
            return redirect('users:loginPage')

        profile = Accounts.objects.filter(email=user).first()

        ''' User verification checks '''
        if not profile.is_verified:
            messages.info(request, 'Your account is not verified!')
            return redirect('users:loginPage')

        if not profile.is_active:
            messages.info(request, 'Your account is not Active!')
            return redirect('users:loginPage')

        auth_user = authenticate(email=email, password=password)
        if auth_user is None:
            messages.warning(request, 'Wrong credentials')
            return redirect('users:loginPage')
        login(request, auth_user)
        return redirect('products:productPage')
    return render(request, 'users/login.html')



def LogOutView(request):
    logout(request)
    return redirect('users:loginPage') 


# customer = request.user.customer
# 		order, created = Order.objects.get_or_create(customer=customer, complete=False)
# 		items = order.orderitem_set.all()
# 		cartItems = order.get_cart_items

@login_required(login_url='users:loginPage')
def userProfile(request):
    vendor = request.user
    products = vendor.products.all() 
    order, created = Order.objects.get_or_create(customer=vendor)
    items = order.orderitem_set.all()

    return render(request,'users/profile.html', {'vendor': vendor, 'products': products,
    'items':items})

