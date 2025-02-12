from django.contrib import admin
from .models import UserProfile,Land,Order,LandAssignment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type','is_available','phone_number', 'aadhar_number', 'gst_number')
    list_filter = ('user_type',)
    search_fields = ('user__email', 'phone_number', 'aadhar_number')

admin.site.register(Land)
admin.site.register(Order)
admin.site.register(LandAssignment)