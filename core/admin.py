from django.contrib import admin
from .models import KitTracking, ExpertSession, StudentReport, AIDoubt, Project, ProjectMember

@admin.register(KitTracking)
class KitTrackingAdmin(admin.ModelAdmin):
    list_display = ['student', 'kit_type', 'kit_name', 'issued_date', 'is_returned']
    list_filter = ['kit_type', 'is_returned']
    search_fields = ['student__user__username', 'kit_name']

@admin.register(ExpertSession)
class ExpertSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'expert_name', 'session_date', 'batch']
    list_filter = ['session_date']
    search_fields = ['title', 'expert_name']

@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'report_type', 'generated_by', 'generated_at']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['student__user__username']

@admin.register(AIDoubt)
class AIDoubtAdmin(admin.ModelAdmin):
    list_display = ['student', 'topic', 'is_helpful', 'created_at']
    list_filter = ['is_helpful', 'created_at']
    search_fields = ['student__user__username', 'question']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'mentor', 'progress_percentage', 'created_at']
    list_filter = ['mentor']
    search_fields = ['title']

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['project', 'student']
    list_filter = ['project']
    search_fields = ['project__title', 'student__user__username']
