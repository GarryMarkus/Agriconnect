from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class UserProfile(models.Model):
    USER_TYPES = [
        ('worker', 'Agricultural Worker'),
        ('provider', 'Land Provider'),
        ('buyer', 'Buyer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile ({self.user_type})"

    def clean(self):
        if self.user_type in ['worker', 'provider'] and not self.aadhar_number:
            raise ValidationError("Aadhar number is required for workers and providers")