from django.urls import path
from .views import homepage

app_name ="homeapp"

urlpatterns = [
    path('', homepage, name='homepage'),      
] 