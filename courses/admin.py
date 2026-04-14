from django.contrib import admin
from .models import (Course, Phase, Module, Topic, Assignment, AssignmentSubmission,
                     StudentProgress, Batch, Notes, Announcement)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_months', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'order', 'requires_mentor_approval', 'requires_exam_pass']
    list_filter = ['course', 'requires_mentor_approval']
    search_fields = ['name', 'course__name']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'phase', 'order']
    list_filter = ['phase__course']
    search_fields = ['name']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'order', 'estimated_hours']
    list_filter = ['module__phase__course']
    search_fields = ['name']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'due_date', 'max_marks']
    list_filter = ['due_date']
    search_fields = ['title']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'status', 'marks_obtained', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['student__user__username', 'assignment__title']

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'topic', 'is_completed', 'completed_at']
    list_filter = ['is_completed']
    search_fields = ['student__user__username', 'topic__name']

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'mentor', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'course']
    search_fields = ['name']

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'batch', 'is_important', 'created_at']
    list_filter = ['is_important', 'created_at']
    search_fields = ['title']
