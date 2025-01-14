from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def start_template(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'login.html')
@csrf_exempt  
def register(request):
    if request.method == 'POST':
        try:
            # Fix: Parse JSON data from request body instead of using POST.get()
            data = json.loads(request.body)
            full_name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')
            user_type = data.get('userType')
            aadhar = data.get('aadhar')
            gst = data.get('gst')
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already registered'
                }, status=400)
            
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name  
            )
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_type,
                phone_number=phone,
                aadhar_number=aadhar if user_type in ['worker', 'provider'] else None,
                gst_number=gst if user_type == 'buyer' else None
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Registration successful',
                'redirect': '/login/'  
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    return render(request, 'register.html')