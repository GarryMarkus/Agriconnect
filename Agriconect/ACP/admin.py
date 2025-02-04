from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'aadhar_number', 'gst_number')
    list_filter = ('user_type',)
    search_fields = ('user__email', 'user__first_name', 'phone_number', 'aadhar_number', 'gst_number')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'phone_number')
        }),
        ('Documents', {
            'fields': ('aadhar_number', 'gst_number')
        }),
    )
