from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_TYPES = [
        ('worker', 'Agricultural Worker'),
        ('provider', 'Land Provider'),
        ('buyer', 'Buyer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    alternate_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    year_of_experience = models.IntegerField( null=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile ({self.user_type})"

    def clean(self):
        if self.user_type in ['worker', 'provider'] and not self.aadhar_number:
            raise ValidationError("Aadhar number is required for workers and providers")
        if self.user_type == 'buyer' and not self.gst_number:
            raise ValidationError("GST number is required for buyers")
class Land(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    total_area = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    survey_number = models.CharField(null=True, max_length=100)
    state = models.CharField(null=True, max_length=100)
    district = models.CharField(max_length=255, default='Default District')  # Fixed typo from 'istrict'
    address = models.TextField(null=True, blank=True)
    previous_crop = models.CharField(null=True, max_length=200)
    irrigation_facilities = models.CharField(max_length=200, null=True)
    ownership_document = models.FileField(null=True, upload_to="documents/")
    survey_document = models.FileField(null=True, upload_to="documents/")
    recent_photos = models.FileField(null=True, upload_to="documents/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Added status field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Land {self.survey_number} - {self.provider.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
