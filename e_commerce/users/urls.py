from django.urls import path
from users.views import RegisterView,LogInView,LogOutView,userProfile

app_name ="users"

urlpatterns = [
    path('login/', LogInView, name='loginPage'),  
    path('sign-up/', RegisterView, name='registerPage'),
    # path('sign-out/', LogOutView.as_view(), name='logoutPage'),
    path('sign-out/', LogOutView, name='logoutPage'),
    path('my-profile/', userProfile, name='profilePage'),
] 