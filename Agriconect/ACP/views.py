from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum 
import json
from django.db import transaction
from .models import UserProfile, Land, Order,LandAssignment
from .utils.gemini_config import get_gemini_response
import asyncio
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

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
@login_required(login_url="/login/")
def submitland(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location = data.get('location')
            size = data.get('size')
            description = data.get('description', '')
            image = request.FILES.get('image')
            land_paper = request.FILES.get('land_paper')
            address = data.get('address')
            irrigation_facilities = data.get('irrigation_facilities')
            district = data.get('district')
            
            if not location or not size or not address or not irrigation_facilities or not district:
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)
            
            land = Land(
                location=location,
                size=size,
                description=description,
                image=image,
                land_paper=land_paper,
                address=address,
                irrigation_facilities=irrigation_facilities,
                district=district,
                provider=request.user
            )
            land.save()
            return JsonResponse({'status':'success','message': 'Land added successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return redirect('provider_dashboard')

@login_required(login_url="/login/")
def worker_dashboard(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'worker':
            return redirect('login')
        return render(request, 'worker.html')
    except UserProfile.DoesNotExist:
        return redirect('login')


@login_required(login_url="/login/")
def submit_land(request):
    if not request.user.userprofile.user_type == 'provider':
        messages.error(request, 'Unauthorized access')
        return redirect('login')

    if request.method == 'POST':
        try:

            irrigation_facilities = request.POST.getlist('irrigation_facilities')
            irrigation_facilities_str = ','.join(irrigation_facilities) if irrigation_facilities else ''

            land = Land(
                provider=request.user,
                total_area=request.POST.get('total_area'),
                survey_number=request.POST.get('survey_number'),
                state=request.POST.get('state'),
                district=request.POST.get('district'),
                address=request.POST.get('address'),
                previous_crop=request.POST.get('previous_crop'),
                irrigation_facilities=irrigation_facilities_str,
            )

            if 'ownership_document' in request.FILES:
                land.ownership_document = request.FILES['ownership_document']
            if 'survey_document' in request.FILES:
                land.survey_document = request.FILES['survey_document']
            if 'recent_photos' in request.FILES:
                land.recent_photos = request.FILES['recent_photos']

            required_fields = ['total_area', 'survey_number', 'state', 'district', 'address']
            for field in required_fields:
                if not getattr(land, field):
                    raise ValueError(f'{field.replace("_", " ").title()} is required')
            land.save()
            messages.success(request, 'Land submitted successfully!')
            return redirect('provider_dashboard')

        except ValueError as ve:
            messages.error(request, str(ve))
            return redirect('submit_land')
        except Exception as e:
            messages.error(request, f'Error submitting land: {str(e)}')
            return redirect('submit_land')
    context = {
        'lands': Land.objects.filter(provider=request.user)
    }
    return render(request, 'landprovider.html', context)
@login_required(login_url="/login/")
def provider_dashboard(request):
    if request.user.userprofile.user_type != 'provider':
        return redirect('login')
    lands = Land.objects.filter(provider=request.user)
    total_area = lands.aggregate(Sum('total_area'))['total_area__sum'] or 0
    active_plots = lands.count()
    pending_approvals = lands.filter(status='pending').count()  
    
    context = {
        'lands': lands,
        'total_area': total_area,
        'active_plots': active_plots,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'landprovider.html', context)
@login_required(login_url="/login/")
def buyer_dashboard(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type != 'buyer':
            return redirect('login')
        return render(request, 'buyer.html')
    except UserProfile.DoesNotExist:
        return redirect('login')

@login_required(login_url="/login/")
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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            user_type = data.get("userType")
            name = data.get("name")
            email = data.get("email")
            phone = data.get("phone")
            password = data.get("password")
            confirm_password = data.get("confirmPassword")
            aadhar = data.get("aadhar", "")
            gst = data.get("gst", "")

            
            if not all([user_type, name, email, phone, password]):
                return JsonResponse({
                    "status": "error",
                    "message": "All required fields must be filled"
                }, status=400)

            if password != confirm_password:
                return JsonResponse({
                    "status": "error",
                    "message": "Passwords do not match"
                }, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Email already registered"
                }, status=400)

            with transaction.atomic():
                User.objects.filter(email=email).delete()
                
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name.split()[0],
                    last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
                )
                UserProfile.objects.filter(user=user).delete()
                
                UserProfile.objects.create(
                    user=user,
                    user_type=user_type,
                    phone_number=phone,
                    aadhar_number=aadhar if user_type in ['worker', 'provider'] else '',
                    gst_number=gst if user_type == 'buyer' else ''
                )

            return JsonResponse({
                "status": "success",
                "message": "Registration successful"
            }, status=201)

        except Exception as e:
            print(f"Registration error: {str(e)}")  
            return JsonResponse({
                "status": "error",
                "message": f"Registration failed: {str(e)}"
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
                return JsonResponse({'status': 'error', 'message': 'No message provided'}, status=400)

            response = await get_gemini_response(user_message)
            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
@login_required(login_url="/login/")
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
@login_required(login_url="/login/")
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not old_password or not new_password1 or not new_password2:
            messages.error(request, "All fields are required!")
            return redirect('change_password')

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect!")
            return redirect('change_password')

        if new_password1 != new_password2:
            messages.error(request, "New passwords don't match!")
            return redirect('change_password')

        try:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, "Password changed successfully! Please login again.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('change_password')

    return render(request, 'changepassword.html')

@login_required
def exit(request):
    logout(request)
    return redirect('/')

@login_required
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('cart')
            total_amount = data.get('totalAmount')
            
            order = Order.objects.create(
                buyer=request.user,
                items=cart_items,
                total_amount=total_amount,
                status='pending' 
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Order created successfully',
                'orderId': order.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def get_order_history(request):
    try:
        orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
        
        active_orders_count = orders.filter(status__in=['pending', 'processing']).count()
        total_purchases = orders.exclude(status='cancelled').count()
        total_amount = orders.exclude(status='cancelled').aggregate(total=Sum('total_amount'))['total'] or 0
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'items': order.items,
                'total_amount': float(order.total_amount),
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'status': order.status
            })
            
        return JsonResponse({
            'status': 'success',
            'orders': orders_data,
            'active_orders_count': active_orders_count,
            'total_purchases': total_purchases,
            'total_spent': float(total_amount)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


@staff_member_required
def admin_dashboard(request):
    context = {
        'pending_orders': Order.objects.filter(status='pending'),
        'free_lands': Land.objects.filter(current_state='free', status='approved'),
        'free_workers': UserProfile.objects.filter(
            user_type='worker', 
            is_available=True  
        ).select_related('user'),
        'active_assignments': LandAssignment.objects.filter(status='active'),
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def assign_land(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            land_id = data.get('land_id')
            worker_id = data.get('worker_id')

            with transaction.atomic():
                order = Order.objects.get(id=order_id)
                land = Land.objects.get(id=land_id)
                worker = User.objects.get(id=worker_id)

            
                assignment = LandAssignment.objects.create(
                    land=land,
                    worker=worker,
                    order=order
                )

                
                land.current_state = "Occupied"
                land.save()

                order.status = 'processing'
                order.save()
                worker.userprofile.is_available = False
                worker.userprofile.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Assignment created successfully'
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@staff_member_required
def complete_assignment(request, assignment_id):
    try:
        with transaction.atomic():
            assignment = LandAssignment.objects.get(id=assignment_id)
            assignment.status = 'completed'
            assignment.save()
            assignment.land.current_state = 'free'
            assignment.land.save()

            worker = assignment.worker
            has_active_assignments = LandAssignment.objects.filter(
                worker=worker, status='active'
            ).exists()
            if not has_active_assignments:
                worker.userprofile.is_available = True  
                worker.userprofile.save()

            order = assignment.order
            if not LandAssignment.objects.filter(order=order, status='active').exists():
                order.status = 'completed'
                order.save()
            
            return JsonResponse({'status': 'success', 'message': 'Assignment completed successfully'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)