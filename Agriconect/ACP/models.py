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
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    is_available = models.BooleanField(default=True)
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
    current_state = [
        ("free","Free"),
        ("occupied","Occupied"),
    ]

    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    total_area = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    survey_number = models.CharField(null=True, max_length=100)
    state = models.CharField(null=True, max_length=100)
    district = models.CharField(max_length=255, default='Default District') 
    address = models.TextField(null=True, blank=True)
    previous_crop = models.CharField(null=True, max_length=200)
    irrigation_facilities = models.CharField(max_length=200, null=True)
    ownership_document = models.FileField(null=True, upload_to="documents/")
    survey_document = models.FileField(null=True, upload_to="documents/")
    recent_photos = models.FileField(null=True, upload_to="documents/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  
    current_state = models.CharField(max_length=10, choices=current_state, default='free')  
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Land {self.survey_number} - {self.provider.username}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.PositiveIntegerField(unique=True, editable=False)    
    items = models.JSONField()  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.order_number} by {self.buyer.username}"

    @classmethod
    def get_next_order_number(cls):
        """Get the next available order number"""
        last_order = cls.objects.order_by('-order_number').first()
        if last_order:
            return last_order.order_number + 1
        return 1

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.get_next_order_number()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class LandAssignment(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_lands')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='active')

    def __str__(self):
        return f"Land {self.land.id} assigned to {self.worker.username} for Order #{self.order.order_number}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('job', 'Job Assignment'),
        ('course', 'New Course'),
        ('general', 'General Update'),
        ('workcompleted', 'Workcompleted'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.user.username}: {self.message}"
