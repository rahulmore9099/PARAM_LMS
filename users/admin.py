from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Staff, ActivityLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'profile_picture', 'date_of_birth', 'address', 'is_verified')}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'user', 'course', 'batch', 'mentor', 'is_active']
    list_filter = ['is_active', 'course', 'batch']
    search_fields = ['enrollment_number', 'user__username', 'user__email']
    raw_id_fields = ['user', 'mentor', 'parent']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'designation', 'department']
    search_fields = ['employee_id', 'user__username', 'designation']
    raw_id_fields = ['user']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'action']
    readonly_fields = ['timestamp']
