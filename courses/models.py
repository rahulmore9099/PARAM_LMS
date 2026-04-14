from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_months = models.IntegerField()
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
    
    def __str__(self):
        return self.name


class Phase(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    requires_mentor_approval = models.BooleanField(default=True)
    requires_exam_pass = models.BooleanField(default=True)
    pass_percentage = models.IntegerField(default=70)
    
    class Meta:
        db_table = 'phases'
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Module(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    
    class Meta:
        db_table = 'modules'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    theory_content = models.TextField(blank=True)
    practical_content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    order = models.IntegerField()
    estimated_hours = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'topics'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Assignment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
        ('resubmit', 'Resubmit Required'),
    )
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assignments'
    
    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    submission_text = models.TextField(blank=True)
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    github_link = models.URLField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Assignment.STATUS_CHOICES, default='submitted')
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'assignment_submissions'
    
    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"


class StudentProgress(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'student_progress'
        unique_together = ['student', 'topic']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.topic.name}"


class Batch(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'mentor'})
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'batches'
    
    def __str__(self):
        return self.name


class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notes'
    
    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
