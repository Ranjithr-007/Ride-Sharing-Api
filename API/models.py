from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

# custom manager for the Users table
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

# table for the user details to be stored
class Users(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=10)
    is_user = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class Rides(models.Model):
    rider = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='rider_booked')
    driver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='driver_booked')
    pickup_location = models.CharField(max_length=30)
    dropoff_location = models.CharField(max_length=30)
    status = models.CharField(max_length=20,default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)