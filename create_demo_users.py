"""
Run this script to create default demo users for all roles.

Usage:
    python manage.py shell < create_demo_users.py
OR:
    python manage.py runscript create_demo_users  (if django-extensions installed)

Direct run from project root:
    cd PARAM_LMS
    python manage.py shell -c "exec(open('create_demo_users.py').read())"
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_lms.settings')
django.setup()

from users.models import User, Student, Staff
from courses.models import Course, Batch

demo_users = [
    {
        'username': 'student',
        'password': 'student123',
        'first_name': 'Demo',
        'last_name': 'Student',
        'email': 'student@paramlms.com',
        'role': 'student',
    },
    {
        'username': 'mentor',
        'password': 'mentor123',
        'first_name': 'Demo',
        'last_name': 'Mentor',
        'email': 'mentor@paramlms.com',
        'role': 'mentor',
    },
    {
        'username': 'admin',
        'password': 'admin123',
        'first_name': 'Demo',
        'last_name': 'Admin',
        'email': 'admin@paramlms.com',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': 'staff',
        'password': 'staff123',
        'first_name': 'Demo',
        'last_name': 'Staff',
        'email': 'staff@paramlms.com',
        'role': 'college_staff',
    },
    {
        'username': 'parent',
        'password': 'parent123',
        'first_name': 'Demo',
        'last_name': 'Parent',
        'email': 'parent@paramlms.com',
        'role': 'parent',
    },
]

created = []
skipped = []

for data in demo_users:
    username = data['username']
    if User.objects.filter(username=username).exists():
        skipped.append(username)
        continue

    user = User.objects.create_user(
        username=username,
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role=data['role'],
        is_verified=True,
        is_staff=data.get('is_staff', False),
        is_superuser=data.get('is_superuser', False),
    )

    # Create Student profile for student user
    if data['role'] == 'student':
        # Get or create a demo course and batch
        course, _ = Course.objects.get_or_create(
            name='Full Stack Python',
            defaults={
                'description': 'Complete Full Stack Python Development course',
                'duration_months': 6,
                'is_active': True,
            }
        )
        mentor_user = User.objects.filter(role='mentor').first()
        batch, _ = Batch.objects.get_or_create(
            name='Batch 2024-A',
            defaults={
                'course': course,
                'mentor': mentor_user,
                'start_date': '2024-01-01',
                'end_date': '2024-06-30',
                'is_active': True,
            }
        )
        Student.objects.create(
            user=user,
            enrollment_number='PARAM2024001',
            course=course,
            batch=batch,
            mentor=mentor_user,
            college_name='Demo College',
            is_active=True,
        )

    # Create Staff profile for staff user
    if data['role'] == 'college_staff':
        Staff.objects.create(
            user=user,
            employee_id='STAFF001',
            department='Computer Science',
            designation='College Coordinator',
            joining_date='2024-01-01',
            college_name='Demo College',
        )

    created.append(username)

print("\n" + "="*50)
print("DEMO USERS SETUP COMPLETE")
print("="*50)

if created:
    print(f"\nCreated ({len(created)}):")
    credentials = {
        'student': 'student123',
        'mentor': 'mentor123',
        'admin': 'admin123',
        'staff': 'staff123',
        'parent': 'parent123',
    }
    for u in created:
        print(f"  {u:10} | password: {credentials.get(u, '???')}")

if skipped:
    print(f"\nSkipped (already exist): {', '.join(skipped)}")

print("\nLogin at: http://127.0.0.1:8000/login/")
print("="*50 + "\n")
