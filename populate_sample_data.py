"""
Sample data population script for Smart LMS
Run: python manage.py shell < populate_sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_lms.settings')
django.setup()

from users.models import User, Student, Staff
from courses.models import Course, Phase, Module, Topic, Batch
from datetime import datetime, timedelta

print("🚀 Starting sample data population...")

# Create Admin User
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@smartlms.com',
        'role': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True,
        'is_verified': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print("✅ Admin user created (username: admin, password: admin123)")

# Create Mentors
mentors = []
mentor_data = [
    ('mentor1', 'John', 'Doe', 'john.mentor@smartlms.com'),
    ('mentor2', 'Sarah', 'Smith', 'sarah.mentor@smartlms.com'),
]

for username, first, last, email in mentor_data:
    mentor, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'role': 'mentor',
            'first_name': first,
            'last_name': last,
            'is_verified': True
        }
    )
    if created:
        mentor.set_password('mentor123')
        mentor.save()
        print(f"✅ Mentor created: {username}")
    mentors.append(mentor)

# Create Courses
courses_data = [
    {
        'name': 'Full Stack Python Django',
        'description': 'Master web development with Python and Django framework',
        'duration_months': 6,
    },
    {
        'name': 'AI ML Data Science',
        'description': 'Become an AI expert with hands-on machine learning projects',
        'duration_months': 8,
    },
    {
        'name': 'DevOps AWS/Azure',
        'description': 'Learn cloud computing and DevOps practices',
        'duration_months': 5,
    },
    {
        'name': 'MERN Stack',
        'description': 'Full stack JavaScript development with MongoDB, Express, React, Node.js',
        'duration_months': 6,
    },
]

courses = []
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        name=course_data['name'],
        defaults=course_data
    )
    if created:
        print(f"✅ Course created: {course.name}")
    courses.append(course)

# Create Phases for Full Stack Python Django
django_course = courses[0]
phases_data = [
    {
        'name': 'Python Basics',
        'description': 'Learn Python fundamentals',
        'order': 1,
    },
    {
        'name': 'Django Framework',
        'description': 'Master Django web framework',
        'order': 2,
    },
    {
        'name': 'REST APIs',
        'description': 'Build RESTful APIs with Django REST Framework',
        'order': 3,
    },
    {
        'name': 'Deployment',
        'description': 'Deploy Django applications to production',
        'order': 4,
    },
]

phases = []
for phase_data in phases_data:
    phase, created = Phase.objects.get_or_create(
        course=django_course,
        order=phase_data['order'],
        defaults=phase_data
    )
    if created:
        print(f"✅ Phase created: {phase.name}")
    phases.append(phase)

# Create Modules for Phase 1 (Python Basics)
python_basics_phase = phases[0]
modules_data = [
    {
        'name': 'Introduction to Python',
        'description': 'Getting started with Python',
        'order': 1,
    },
    {
        'name': 'Data Structures',
        'description': 'Lists, Tuples, Dictionaries, Sets',
        'order': 2,
    },
    {
        'name': 'Functions and Modules',
        'description': 'Creating reusable code',
        'order': 3,
    },
]

modules = []
for module_data in modules_data:
    module, created = Module.objects.get_or_create(
        phase=python_basics_phase,
        order=module_data['order'],
        defaults=module_data
    )
    if created:
        print(f"✅ Module created: {module.name}")
    modules.append(module)

# Create Topics for first module
intro_module = modules[0]
topics_data = [
    {
        'name': 'Python Installation and Setup',
        'theory_content': 'Learn how to install Python and set up your development environment',
        'order': 1,
        'estimated_hours': 2,
    },
    {
        'name': 'Variables and Data Types',
        'theory_content': 'Understanding Python variables, numbers, strings, and booleans',
        'order': 2,
        'estimated_hours': 3,
    },
    {
        'name': 'Control Flow',
        'theory_content': 'If statements, loops, and conditional logic',
        'order': 3,
        'estimated_hours': 4,
    },
]

for topic_data in topics_data:
    topic, created = Topic.objects.get_or_create(
        module=intro_module,
        order=topic_data['order'],
        defaults=topic_data
    )
    if created:
        print(f"✅ Topic created: {topic.name}")

# Create Batches
batches_data = [
    {
        'name': 'Batch 2024-A',
        'course': django_course,
        'mentor': mentors[0],
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
    {
        'name': 'Batch 2024-B',
        'course': courses[1],  # AI ML
        'mentor': mentors[1],
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=240)).date(),
    },
]

batches = []
for batch_data in batches_data:
    batch, created = Batch.objects.get_or_create(
        name=batch_data['name'],
        defaults=batch_data
    )
    if created:
        print(f"✅ Batch created: {batch.name}")
    batches.append(batch)

# Create Students
students_data = [
    ('student1', 'Alice', 'Johnson', 'alice@example.com', 'ENR001'),
    ('student2', 'Bob', 'Williams', 'bob@example.com', 'ENR002'),
    ('student3', 'Charlie', 'Brown', 'charlie@example.com', 'ENR003'),
]

for username, first, last, email, enr_no in students_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'role': 'student',
            'first_name': first,
            'last_name': last,
            'is_verified': True
        }
    )
    if created:
        user.set_password('student123')
        user.save()
        
        # Create student profile
        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'enrollment_number': enr_no,
                'batch': batches[0],
                'course': django_course,
                'mentor': mentors[0],
                'current_phase': phases[0],
            }
        )
        print(f"✅ Student created: {username} ({enr_no})")

# Create Parent
parent, created = User.objects.get_or_create(
    username='parent1',
    defaults={
        'email': 'parent@example.com',
        'role': 'parent',
        'first_name': 'Parent',
        'last_name': 'User',
        'is_verified': True
    }
)
if created:
    parent.set_password('parent123')
    parent.save()
    print("✅ Parent user created")

# Create College Staff
staff_user, created = User.objects.get_or_create(
    username='staff1',
    defaults={
        'email': 'staff@example.com',
        'role': 'college_staff',
        'first_name': 'Staff',
        'last_name': 'Member',
        'is_verified': True
    }
)
if created:
    staff_user.set_password('staff123')
    staff_user.save()
    
    Staff.objects.get_or_create(
        user=staff_user,
        defaults={
            'employee_id': 'EMP001',
            'department': 'Academic',
            'designation': 'Coordinator',
            'joining_date': datetime.now().date(),
        }
    )
    print("✅ Staff user created")

print("\n" + "="*50)
print("🎉 Sample data population completed!")
print("="*50)
print("\n📋 Login Credentials:")
print("-" * 50)
print("Admin:")
print("  Username: admin")
print("  Password: admin123")
print("\nMentor:")
print("  Username: mentor1")
print("  Password: mentor123")
print("\nStudent:")
print("  Username: student1")
print("  Password: student123")
print("\nParent:")
print("  Username: parent1")
print("  Password: parent123")
print("\nStaff:")
print("  Username: staff1")
print("  Password: staff123")
print("-" * 50)
print("\n🌐 Access the application at: http://127.0.0.1:8000/")
print("🔧 Admin panel at: http://127.0.0.1:8000/admin/")
print("\n✨ Happy Learning!")
