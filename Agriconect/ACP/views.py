from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile, Land
from .utils.gemini_config import get_gemini_response
import asyncio

def start_template(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('userType')

            if not email or not password or not user_type:
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.user_type != user_type:
                        return JsonResponse({'status': 'error', 'message': 'User type does not match'}, status=400)

                    auth_login(request, user)

                    if user_profile.user_type == 'worker':
                        return JsonResponse({'status': 'success', 'redirect': '/worker_dashboard/'})
                    elif user_profile.user_type == 'provider':
                        return JsonResponse({'status': 'success', 'redirect': '/provider_dashboard/'})
                    elif user_profile.user_type == 'buyer':
                        return JsonResponse({'status': 'success', 'redirect': '/buyer_dashboard/'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid user type'}, status=400)

                except UserProfile.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'User profile does not exist'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'login.html')

@login_required
def worker_dashboard(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'worker':
            return redirect('login')

        lands = Land.objects.filter(status='available')
        return render(request, 'worker.html', {'lands': lands})
    except UserProfile.DoesNotExist:
        return redirect('login')

# @login_required
# def request_land_use(request, land_id):
#     land = get_object_or_404(Land, id=land_id)

#     if request.user.userprofile.user_type != 'worker':
#         return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

#     existing_request = LandRequest.objects.filter(worker=request.user, land=land).exists()
#     if existing_request:
#         return JsonResponse({'status': 'error', 'message': 'Request already sent'}, status=400)

#     LandRequest.objects.create(worker=request.user, land=land)
#     return JsonResponse({'status': 'success', 'message': 'Land use request sent successfully'})

# @login_required
# def provider_dashboard(request):
#     if request.user.userprofile.user_type != 'provider':
#         return redirect('login')

#     lands = Land.objects.filter(provider=request.user)
#     land_requests = LandRequest.objects.filter(land__provider=request.user, status='pending')
    
#     return render(request, 'provider_dashboard.html', {'lands': lands, 'land_requests': land_requests})

# @login_required
# def approve_land_request(request, request_id):
#     land_request = get_object_or_404(LandRequest, id=request_id, land__provider=request.user)

#     land_request.status = 'approved'
#     land_request.land.status = 'in_use'
#     land_request.land.save()
#     land_request.save()

#     return JsonResponse({'status': 'success', 'message': 'Land request approved'})

# @login_required
# def reject_land_request(request, request_id):
#     land_request = get_object_or_404(LandRequest, id=request_id, land__provider=request.user)

#     land_request.status = 'rejected'
#     land_request.save()

#     return JsonResponse({'status': 'success', 'message': 'Land request rejected'})

@login_required
def add_land(request):
    if request.user.userprofile.user_type != 'provider':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

    if request.method == 'POST':
        try:
            location = request.POST.get('location')
            size = request.POST.get('size')
            description = request.POST.get('description', '')
            image = request.FILES.get('image')
            land_paper = request.FILES.get('land_paper')

            if not location or not size:
                return JsonResponse({'status': 'error', 'message': 'Location and size are required'}, status=400)

            Land.objects.create(
                provider=request.user,
                location=location,
                size=size,
                description=description,
                image=image,
                land_paper=land_paper
            )

            return JsonResponse({'status': 'success', 'message': 'Land added successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'add_land.html')


@login_required
def buyer_dashboard(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'buyer':
            return redirect('login')
        return render(request, 'buyer_dashboard.html')
    except UserProfile.DoesNotExist:
        return redirect('login')

@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type not in ['worker', 'provider', 'buyer']:
            return redirect('login')
        return render(request, 'profile.html', {'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        return redirect('login')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['name', 'email', 'password', 'phone', 'userType']
            if not all(data.get(field) for field in required_fields):
                return JsonResponse({'status': 'error', 'message': 'All required fields must be filled'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)

            user = User.objects.create_user(username=data['email'], email=data['email'], password=data['password'], first_name=data['name'])
            UserProfile.objects.create(
                user=user,
                user_type=data['userType'],
                phone_number=data['phone'],
                aadhar_number=data.get('aadhar') if data['userType'] in ['worker', 'provider'] else None,
                gst_number=data.get('gst') if data['userType'] == 'buyer' else None
            )

            return JsonResponse({'status': 'success', 'message': 'Registration successful', 'redirect': '/login/'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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
                return JsonResponse({'status': 'error', 'message': 'No message provided'}, status=400)

            response = await get_gemini_response(user_message)
            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
@login_required
def update_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_profile.father_name = request.POST.get('father-name', user_profile.father_name)
        user_profile.dob = request.POST.get('dob', user_profile.dob)
        user_profile.phone_number = request.POST.get('contact-number', user_profile.phone_number)
        user_profile.alternate_contact = request.POST.get('alternate-contact', user_profile.alternate_contact)
        user_profile.address = request.POST.get('address', user_profile.address)
        user_profile.city = request.POST.get('town', user_profile.city)
        user_profile.pin_code = request.POST.get('pin-code', user_profile.pin_code)
        user_profile.year_of_experience = request.POST.get('year', user_profile.year_of_experience)

        user_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile') 
    return render(request, 'profile.html', {'user_profile': user_profile})
@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            new_password1 = data.get('new_password')
            new_password2 = data.get('new_password')
        
            if not request.user.check_password(old_password):
                messages.error(request, "Incorrect old password!")
                return redirect('/profile/')
        
            if new_password1 != new_password2:
                messages.error(request, "Passwords didn't match!")
                return redirect('/profile/')
        
            user = request.user
            user.set_password(new_password1)
            user.save()
        
            messages.success(request, "Password changed successfully!")
            return redirect('/profile/')
        except json.JSONDecodeError:
            messages.error(request, "Invalid JSON format!")
            return redirect('/profile/')
    
    return render(request, 'changepassword.html')

@login_required
def exit(request):
    logout(request)
    return redirect('/')