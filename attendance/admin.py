from django.contrib import admin
from .models import Attendance, LeaveRequest, QRAttendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date']
    search_fields = ['student__user__username']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'from_date', 'to_date', 'status', 'approved_by']
    list_filter = ['status', 'from_date']
    search_fields = ['student__user__username']

@admin.register(QRAttendance)
class QRAttendanceAdmin(admin.ModelAdmin):
    list_display = ['batch', 'date', 'is_active', 'created_by']
    list_filter = ['is_active', 'date']
    search_fields = ['batch__name']
