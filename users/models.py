from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('college_staff', 'College Staff'),
        ('parent', 'Parent'),
        ('mentor', 'Institute Mentor'),
        ('hr', 'HR'),
        ('accounts', 'Accounts'),
        ('business_dev', 'Business Development'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=50, unique=True)
    batch = models.ForeignKey('courses.Batch', on_delete=models.SET_NULL, null=True, related_name='students')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mentored_students', limit_choices_to={'role': 'mentor'})
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children', limit_choices_to={'role': 'parent'})
    college_name = models.CharField(max_length=200, blank=True)
    current_phase = models.ForeignKey('courses.Phase', on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    residence_type = models.CharField(
        max_length=20,
        choices=[('hostel', 'Hostel'), ('home', 'Home'), ('guardian', 'Guardian')],
        blank=True
    )
    parent_name = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'students'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.enrollment_number}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    college_name = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'staff'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=200)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action}"
