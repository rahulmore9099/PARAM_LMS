from django.db import models
from django.conf import settings

class KitTracking(models.Model):
    KIT_TYPE_CHOICES = (
        ('laptop', 'Laptop'),
        ('iot_kit', 'IoT Kit'),
        ('books', 'Books'),
        ('id_card', 'ID Card'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='kits')
    kit_type = models.CharField(max_length=20, choices=KIT_TYPE_CHOICES)
    kit_name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, blank=True)
    issued_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    condition = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'kit_tracking'
    
    def __str__(self):
        return f"{self.student.user.username} - {self.kit_name}"


class ExpertSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    expert_name = models.CharField(max_length=200)
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    meeting_link = models.URLField(blank=True)
    recording_link = models.URLField(blank=True)
    batch = models.ForeignKey('courses.Batch', on_delete=models.CASCADE, related_name='expert_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'expert_sessions'
        ordering = ['-session_date']
    
    def __str__(self):
        return self.title


class StudentReport(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='reports')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.report_type}"


class AIDoubt(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='ai_doubts')
    question = models.TextField()
    answer = models.TextField()
    topic = models.ForeignKey('courses.Topic', on_delete=models.SET_NULL, null=True, blank=True)
    is_helpful = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_doubts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.question[:50]}"



class TopPerformer(models.Model):
    PERIOD_CHOICES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    )
    
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='top_performances')
    batch = models.ForeignKey('courses.Batch', on_delete=models.CASCADE, related_name='top_performers')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    rank = models.IntegerField()  # 1-5
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_performers')
    approved_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'top_performers'
        ordering = ['batch', 'year', 'month', 'rank']
        unique_together = ['student', 'batch', 'period', 'month', 'year']
    
    def __str__(self):
        return f"{self.student.user.username} - Rank {self.rank} - {self.month}/{self.year}"


class ExamSchedule(models.Model):
    exam = models.OneToOneField('exams.Exam', on_delete=models.CASCADE, related_name='schedule')
    batch = models.ForeignKey('courses.Batch', on_delete=models.CASCADE, related_name='exam_schedules')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    venue = models.CharField(max_length=200, blank=True)
    instructions = models.TextField(blank=True)
    is_announced = models.BooleanField(default=False)
    announced_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exam_schedules'
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.exam.title} - {self.scheduled_date}"
