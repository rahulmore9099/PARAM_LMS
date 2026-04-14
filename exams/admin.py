from django.contrib import admin
from .models import Exam, Question, ExamAttempt, Answer, MockTest

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_type', 'phase', 'duration_minutes', 'total_marks', 'is_active']
    list_filter = ['exam_type', 'is_active']
    search_fields = ['title']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'question_type', 'marks', 'order']
    list_filter = ['question_type', 'exam']
    search_fields = ['question_text']

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'status', 'marks_obtained', 'is_passed', 'start_time']
    list_filter = ['status', 'is_passed']
    search_fields = ['student__user__username', 'exam__title']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'marks_obtained', 'is_correct']
    list_filter = ['is_correct']

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'phase', 'duration_minutes', 'total_marks']
    search_fields = ['title']
