from django.contrib import admin
from .models import Student, CustomUser, Profile, Profile1

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active', 'groups')
    ordering = ('email',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'rollnumber', 'email', 'percentage', 'user')
    search_fields = ('name', 'email', 'rollnumber')
    list_filter = ('percentage',)
    ordering = ('rollnumber',)

# Register Profile and Profile1 models if needed
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile1)
class Profile1Admin(admin.ModelAdmin):
    pass

