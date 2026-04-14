from django.db import models
from django.conf import settings

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('mcq', 'MCQ Quiz'),
        ('practical', 'Practical Coding Test'),
        ('mock', 'Mock Interview'),
        ('final', 'Final Assessment'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    phase = models.ForeignKey('courses.Phase', on_delete=models.CASCADE, related_name='exams')
    duration_minutes = models.IntegerField()
    total_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exams'
    
    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('mcq', 'Multiple Choice'),
        ('coding', 'Coding Problem'),
        ('descriptive', 'Descriptive'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    marks = models.IntegerField()
    order = models.IntegerField()
    
    # For MCQ
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_option = models.CharField(max_length=1, blank=True)
    
    # For Coding
    test_cases = models.JSONField(blank=True, null=True)
    starter_code = models.TextField(blank=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.order}"


class ExamAttempt(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='exam_attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    marks_obtained = models.IntegerField(null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'exam_attempts'
    
    def __str__(self):
        return f"{self.student.user.username} - {self.exam.title}"


class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.CharField(max_length=1, blank=True)
    code_submission = models.TextField(blank=True)
    marks_obtained = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'answers'
    
    def __str__(self):
        return f"{self.attempt.student.user.username} - {self.question.question_text[:50]}"


class MockTest(models.Model):
    title = models.CharField(max_length=200)
    phase = models.ForeignKey('courses.Phase', on_delete=models.CASCADE, related_name='mock_tests')
    duration_minutes = models.IntegerField()
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mock_tests'
    
    def __str__(self):
        return self.title
