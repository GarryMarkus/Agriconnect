from django.urls import path
from ACP.views import *

urlpatterns = [
    path('', index, name='index'),
    path("login/",login,name="login"),
    path("register/",register,name="register"),
    path('chatbot/response/', chatbot_response, name='chatbot_response'),
    path('worker_dashboard/',worker_dashboard, name='worker_dashboard'),
    path("profile/",profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('change_password/',change_password, name='change_password'),
    path("logout/",exit, name='logout'),
    path("provider_dashboard/",provider_dashboard,name="provider"),
    path('submit_land/',submit_land, name='submit_land'),
    path("buyer_dashboard/",buyer_dashboard, name="buyer"),
    path('create_order/', create_order, name='create_order'),
    path('get_order_history/', get_order_history, name='get_order_history'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-assign-land/',assign_land, name='assign_land'),
    path('admin-complete-assignment/<int:assignment_id>/', complete_assignment, name='complete_assignment'),
]