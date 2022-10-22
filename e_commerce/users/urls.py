from django.urls import path
from users.views import RegisterView,LogInView,LogOutView,index



app_name ="users"

urlpatterns = [
    path('', LogInView, name='loginPage'),  
    path('sign-up/', RegisterView, name='registerPage'),
    path('sign-out/', LogOutView.as_view(), name='logoutPage'),
    path('home/', index, name='homepage'),      
] 