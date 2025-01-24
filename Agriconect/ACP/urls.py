from django.urls import path
from ACP.views import *

urlpatterns = [
    path('', index, name='index'),
    path("login/",login,name="login"),
    path("register/",register,name="register"),
    path('chatbot/response/', chatbot_response, name='chatbot_response'),
]