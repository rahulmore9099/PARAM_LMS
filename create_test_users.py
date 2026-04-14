"""
Create test users for Smart LMS
Run this script: python create_test_users.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_lms.settings')
django.setup()

from users.models import User, Student, Staff
from courses.models import Course, Batch

def create_test_users():
    print("Creating test users...")
    
    # Create Course first
    course, created = Course.objects.get_or_create(
        name="Full Stack Python Django",
        defaults={
            'description': 'Complete Python Django course with projects',
            'duration_months': 6,
            'is_active': True
        }
    )
    if created:
        print(f"✓ Created course: {course.name}")
    
    # Create Batch
    from datetime import date, timedelta
    batch, created = Batch.objects.get_or_create(
        name="Batch 2024-A",
        defaults={
            'course': course,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=180),
            'is_active': True
        }
    )
    if created:
        print(f"✓ Created batch: {batch.name}")
    
    # 1. Create Student User
    try:
        student_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='student123',
            first_name='Rahul',
            last_name='Kumar',
            role='student',
            phone='9876543210',
            is_verified=True
        )
        
        # Create Student Profile
        Student.objects.create(
            user=student_user,
            enrollment_number='STU2024001',
            course=course,
            batch=batch,
            college_name='ABC College',
            is_active=True
        )
        print("✓ Created Student: username='student', password='student123'")
    except Exception as e:
        print(f"✗ Student already exists or error: {e}")
    
    # 2. Create Mentor User
    try:
        mentor_user = User.objects.create_user(
            username='mentor',
            email='mentor@example.com',
            password='mentor123',
            first_name='Priya',
            last_name='Sharma',
            role='mentor',
            phone='9876543211',
            is_verified=True
        )
        print("✓ Created Mentor: username='mentor', password='mentor123'")
    except Exception as e:
        print(f"✗ Mentor already exists or error: {e}")
    
    # 3. Create Staff User
    try:
        staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='staff123',
            first_name='Amit',
            last_name='Verma',
            role='staff',
            phone='9876543212',
            is_verified=True
        )
        
        # Create Staff Profile
        Staff.objects.create(
            user=staff_user,
            employee_id='EMP2024001',
            department='Administration',
            is_active=True
        )
        print("✓ Created Staff: username='staff', password='staff123'")
    except Exception as e:
        print(f"✗ Staff already exists or error: {e}")
    
    # 4. Create Parent User
    try:
        parent_user = User.objects.create_user(
            username='parent',
            email='parent@example.com',
            password='parent123',
            first_name='Rajesh',
            last_name='Kumar',
            role='parent',
            phone='9876543213',
            is_verified=True
        )
        print("✓ Created Parent: username='parent', password='parent123'")
    except Exception as e:
        print(f"✗ Parent already exists or error: {e}")
    
    # 5. Create HR User
    try:
        hr_user = User.objects.create_user(
            username='hr',
            email='hr@example.com',
            password='hr123',
            first_name='Neha',
            last_name='Singh',
            role='hr',
            phone='9876543214',
            is_verified=True
        )
        print("✓ Created HR: username='hr', password='hr123'")
    except Exception as e:
        print(f"✗ HR already exists or error: {e}")
    
    # 6. Create Accounts User
    try:
        accounts_user = User.objects.create_user(
            username='accounts',
            email='accounts@example.com',
            password='accounts123',
            first_name='Suresh',
            last_name='Patel',
            role='accounts',
            phone='9876543215',
            is_verified=True
        )
        print("✓ Created Accounts: username='accounts', password='accounts123'")
    except Exception as e:
        print(f"✗ Accounts already exists or error: {e}")
    
    # 7. Create Business Dev User
    try:
        bizdev_user = User.objects.create_user(
            username='bizdev',
            email='bizdev@example.com',
            password='bizdev123',
            first_name='Vikram',
            last_name='Malhotra',
            role='business_dev',
            phone='9876543216',
            is_verified=True
        )
        print("✓ Created Business Dev: username='bizdev', password='bizdev123'")
    except Exception as e:
        print(f"✗ Business Dev already exists or error: {e}")
    
    print("\n" + "="*60)
    print("TEST USERS CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nLogin Credentials:")
    print("-" * 60)
    print("Admin:        username='admin'     password='admin123'")
    print("Student:      username='student'   password='student123'")
    print("Mentor:       username='mentor'    password='mentor123'")
    print("Staff:        username='staff'     password='staff123'")
    print("Parent:       username='parent'    password='parent123'")
    print("HR:           username='hr'        password='hr123'")
    print("Accounts:     username='accounts'  password='accounts123'")
    print("Business Dev: username='bizdev'    password='bizdev123'")
    print("-" * 60)
    print("\nLogin URL: http://127.0.0.1:8000/login/")
    print("="*60)

if __name__ == '__main__':
    create_test_users()
