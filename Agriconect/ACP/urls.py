from django.urls import path
from ACP.views import *

urlpatterns = [
    path('',start_template, name='home'),
    path("login/",login,name="login"),
    path("register/",register,name="register")
    
    ]