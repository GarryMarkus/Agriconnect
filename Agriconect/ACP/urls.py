from django.urls import path
from ACP.views import *

urlpatterns = [
    path('',start_template, name='home'),
    ]