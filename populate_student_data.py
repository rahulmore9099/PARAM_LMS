import os
import django
from datetime import datetime, timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_lms.settings')
django.setup()

from users.models import User, Student
from courses.models import Course, Phase, Module, Topic, Assignment, StudentProgress, AssignmentSubmission
from exams.models import Exam, Question, ExamAttempt
from attendance.models import Attendance

def populate_data():
    print("Starting data population...")
    
    # Get student user
    try:
        student_user = User.objects.get(username='student')
        student = student_user.student_profile
        print(f"Found student: {student.enrollment_number}")
    except:
        print("Student not found! Please run create_test_users.py first")
        return
    
    # Get or create course
    course, created = Course.objects.get_or_create(
        name="Full Stack Python Django",
        defaults={
            'description': 'Complete Full Stack Web Development with Python and Django',
            'duration_months': 6,
            'is_active': True
        }
    )
    print(f"Course: {course.name}")
    
    # Assign course to student
    student.course = course
    student.save()
    
    # Create Phase 0: Python Fundamentals
    phase0, created = Phase.objects.get_or_create(
        course=course,
        order=0,
        defaults={
            'name': 'Phase 0: Python Fundamentals',
            'description': 'Learn Python basics and fundamentals',
            'requires_mentor_approval': True,
            'requires_exam_pass': True,
            'pass_percentage': 70
        }
    )
    
    # Set current phase
    student.current_phase = phase0
    student.save()
    
    # Create Module 1 for Phase 0
    module1, created = Module.objects.get_or_create(
        phase=phase0,
        order=1,
        defaults={
            'name': 'Introduction to Python',
            'description': 'Python basics and setup'
        }
    )
    
    # Create Topics for Module 1
    topics_data = [
        {
            'name': 'What is Machine Learning?',
            'theory_content': 'Introduction to ML concepts',
            'estimated_hours': 1,
            'order': 1
        },
        {
            'name': 'Three Types of Machine Learning',
            'theory_content': 'Supervised, Unsupervised, Reinforcement',
            'estimated_hours': 1,
            'order': 2
        },
        {
            'name': 'ML Workflow: Data → Model → Prediction',
            'theory_content': 'Complete previous lesson to unlock',
            'estimated_hours': 1,
            'order': 3
        },
        {
            'name': 'Setting up Python Environment',
            'theory_content': 'Practical coding session',
            'estimated_hours': 2,
            'order': 4
        },
        {
            'name': 'Quiz: Module 1 Assessment',
            'theory_content': 'Test your knowledge',
            'estimated_hours': 1,
            'order': 5
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            module=module1,
            order=topic_data['order'],
            defaults={
                'name': topic_data['name'],
                'theory_content': topic_data['theory_content'],
                'estimated_hours': topic_data['estimated_hours']
            }
        )
        
        # Mark first topic as completed
        if topic_data['order'] == 1:
            StudentProgress.objects.get_or_create(
                student=student,
                topic=topic,
                defaults={
                    'is_completed': True,
                    'completed_at': datetime.now()
                }
            )
            print(f"✓ Completed: {topic.name}")
        else:
            print(f"  Created: {topic.name}")
    
    # Create Phase 1: Intro to Machine Learning
    phase1, created = Phase.objects.get_or_create(
        course=course,
        order=1,
        defaults={
            'name': 'Phase 1: Intro to Machine Learning',
            'description': 'Introduction to Machine Learning concepts',
            'requires_mentor_approval': True,
            'requires_exam_pass': True,
            'pass_percentage': 70
        }
    )
    
    # Create Phase 2: Advanced ML
    phase2, created = Phase.objects.get_or_create(
        course=course,
        order=2,
        defaults={
            'name': 'Phase 2: Advanced ML',
            'description': 'Advanced Machine Learning techniques',
            'requires_mentor_approval': True,
            'requires_exam_pass': True,
            'pass_percentage': 70
        }
    )
    
    # Create Phase 3: Deep Learning
    phase3, created = Phase.objects.get_or_create(
        course=course,
        order=3,
        defaults={
            'name': 'Phase 3: Deep Learning',
            'description': 'Neural Networks and Deep Learning',
            'requires_mentor_approval': True,
            'requires_exam_pass': True,
            'pass_percentage': 70
        }
    )
    
    # Create some assignments
    topic1 = Topic.objects.filter(module=module1).first()
    if topic1:
        assignment1, created = Assignment.objects.get_or_create(
            topic=topic1,
            title='Python Basics Assignment',
            defaults={
                'description': 'Complete exercises on Python variables, data types, and operators',
                'due_date': datetime.now() + timedelta(days=7),
                'max_marks': 100
            }
        )
        print(f"Created assignment: {assignment1.title}")
        
        assignment2, created = Assignment.objects.get_or_create(
            topic=topic1,
            title='Functions and Modules Project',
            defaults={
                'description': 'Build a calculator using Python functions',
                'due_date': datetime.now() + timedelta(days=14),
                'max_marks': 100
            }
        )
        print(f"Created assignment: {assignment2.title}")
    
    # Create an exam
    exam1, created = Exam.objects.get_or_create(
        title='Phase 0 Final Assessment',
        phase=phase0,
        defaults={
            'description': 'Final exam for Python Fundamentals',
            'exam_type': 'mcq',
            'duration_minutes': 60,
            'total_marks': 100,
            'pass_marks': 70,
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(days=30),
            'is_active': True
        }
    )
    
    if created:
        # Create some questions
        Question.objects.create(
            exam=exam1,
            question_text='What is Python?',
            question_type='mcq',
            marks=10,
            order=1,
            option_a='A programming language',
            option_b='A snake',
            option_c='A framework',
            option_d='A database',
            correct_option='A'
        )
        
        Question.objects.create(
            exam=exam1,
            question_text='Which keyword is used to define a function in Python?',
            question_type='mcq',
            marks=10,
            order=2,
            option_a='function',
            option_b='def',
            option_c='func',
            option_d='define',
            correct_option='B'
        )
        print(f"Created exam: {exam1.title} with questions")
    
    # Create attendance records
    for i in range(10):
        attendance_date = date.today() - timedelta(days=i)
        status = 'present' if i < 8 else 'absent'
        
        if status == 'present':
            Attendance.objects.get_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    'status': status,
                    'in_time': '09:00',
                    'out_time': '17:00',
                    'in_latitude': 28.6139,
                    'in_longitude': 77.2090,
                    'in_location_address': 'Training Institute, New Delhi',
                    'out_latitude': 28.6139,
                    'out_longitude': 77.2090,
                    'out_location_address': 'Training Institute, New Delhi'
                }
            )
        else:
            Attendance.objects.get_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    'status': status
                }
            )
    print(f"Created 10 attendance records")
    
    print("\n✅ Data population completed successfully!")
    print("\nSummary:")
    print(f"- Course: {course.name}")
    print(f"- Phases: {Phase.objects.filter(course=course).count()}")
    print(f"- Modules: {Module.objects.filter(phase__course=course).count()}")
    print(f"- Topics: {Topic.objects.filter(module__phase__course=course).count()}")
    print(f"- Assignments: {Assignment.objects.filter(topic__module__phase__course=course).count()}")
    print(f"- Exams: {Exam.objects.filter(phase__course=course).count()}")
    print(f"- Attendance Records: {Attendance.objects.filter(student=student).count()}")
    print(f"- Completed Topics: {StudentProgress.objects.filter(student=student, is_completed=True).count()}")

if __name__ == '__main__':
    populate_data()
