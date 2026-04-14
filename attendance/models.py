from django.db import models
from django.conf import settings

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    )
    
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    
    # Time tracking
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    
    # Location tracking
    in_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    in_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    in_location_address = models.CharField(max_length=500, blank=True)
    
    out_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    out_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    out_location_address = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='leave_requests')
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.from_date} to {self.to_date}"


class QRAttendance(models.Model):
    batch = models.ForeignKey('courses.Batch', on_delete=models.CASCADE, related_name='qr_attendances')
    qr_code = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'qr_attendance'
    
    def __str__(self):
        return f"{self.batch.name} - {self.date}"
