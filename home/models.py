from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .manager import CustomUserManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)


class Profile1(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = None
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    rollnumber = models.IntegerField(default=0, unique=True)
    physics = models.IntegerField(default=0)
    chemistry = models.IntegerField(default=0)
    maths = models.IntegerField(default=0)
    english = models.IntegerField(default=0)
    totalmarks = models.IntegerField(default=0)
    maxmarks = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Associate each student with a user

    class Meta:
        permissions = [
            ("can_access_landing_page", "Can access landing page"),
            ("can_upload_excel", "Can upload excel files"),
            ("can_view_studentlist", "Can view student list"),
            ("can_view_student_info", "Can view student info"),
            ("can_view_student_score", "Can view student score"),
        ]


class UploadFileForm(models.Model): 
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True) 





    


