from django.contrib import admin
from .models import Land, LandAssignment, Order, UserProfile,Notification
from django.urls import reverse
from django.utils.html import format_html

admin.site.site_header = "Agriconnect Admin"
admin.site.index_title = "Welcome to Agriconnect Admin"



@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_number', 'provider', 'status', 'current_state', 'total_area', 'district')
    search_fields = ('survey_number', 'provider__username', 'district')
    list_filter = ('status', 'current_state')

@admin.register(LandAssignment)
class LandAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'land', 'worker', 'order', 'status', 'assigned_date')
    search_fields = ('land__survey_number', 'worker__username', 'order__order_number')
    list_filter = ('status',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'order_number', 'total_amount', 'status', 'created_at')
    search_fields = ('buyer__username', 'order_number')
    list_filter = ('status',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_type', 'phone_number', 'is_available')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('user_type', 'is_available')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('user__username', 'message')