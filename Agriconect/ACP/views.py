from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import authenticate
from .utils.gemini_config import get_gemini_response
import asyncio

def start_template(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if hasattr(user, 'profile') and user.profile.user_type == role:
                auth_login(request, user)
                if role == 'provider':
                    return redirect('provider_dashboard')
                elif role == 'worker':
                    return redirect('worker_dashboard')
                elif role == 'buyer':
                    return redirect('buyer_dashboard')
            else:
                messages.error(request, 'Invalid role')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'login.html')

@login_required
def buyer_dashboard(request):
    if request.user.profile.user_type != 'buyer':
        return redirect('login')
    return render(request, 'buyer_dashboard.html')

@login_required
def worker_dashboard(request):
    if request.user.profile.user_type != 'worker':
        return redirect('login')
    return render(request, 'worker.html')

@login_required
def provider_dashboard(request):
    if request.user.profile.user_type != 'provider':
        return redirect('login')
    return render(request, 'provider_dashboard.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['name', 'email', 'password', 'phone', 'userType']
            if not all(data.get(field) for field in required_fields):
                return JsonResponse({
                    'status': 'error',
                    'message': 'All required fields must be filled'
                }, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already registered'
                }, status=400)

            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['name']
            )
            profile = UserProfile.objects.create(
                user=user,
                user_type=data['userType'],
                phone_number=data['phone'],
                aadhar_number=data.get('aadhar') if data['userType'] in ['worker', 'provider'] else None,
                gst_number=data.get('gst') if data['userType'] == 'buyer' else None
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

def index(request):
    return render(request, 'index.html')

@csrf_exempt
async def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No message provided'
                }, status=400)

            response = await get_gemini_response(user_message)
            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)
        except Exception as e:
            print(f"Error in chatbot_response: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)