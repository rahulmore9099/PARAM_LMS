# 🚀 Smart LMS - Login Credentials & Access Guide

## 🌐 Server Information
- **URL**: http://127.0.0.1:8000/
- **Status**: ✅ Running
- **Django Version**: 5.2.10

---

## 🔐 All Login Credentials

### 1. 👨‍💼 Admin Panel Access
**Role**: Super Administrator
- **Username**: `admin`
- **Password**: `admin123`
- **Dashboard**: `/dashboard/admin/`
- **Django Admin**: `/admin/`

**Features**:
- Complete system control
- Students CRUD operations
- Courses & Batches management
- Exams creation
- Mentors management
- Attendance management
- Announcements
- All reports and analytics

---

### 2. 🎓 Student Panel Access
**Role**: Student
- **Username**: `student`
- **Password**: `student123`
- **Dashboard**: `/dashboard/student/`
- **Enrollment**: `STU2024001`

**Features**:
- Course progress tracking
- Assignment submissions
- Exam attempts
- Attendance marking (GPS-based)
- AI Help assistant
- Video explanations
- Progress charts
- My rank (if in top 5)

---

### 3. 👨‍🏫 Mentor Panel Access
**Role**: Mentor/Teacher
- **Username**: `mentor`
- **Password**: `mentor123`
- **Dashboard**: `/dashboard/mentor/`

**Features**:
- Student progress monitoring
- Assignment evaluation
- Exam grading
- Attendance tracking
- Top performers approval
- Student list management

---

### 4. 👨‍👩‍👧 Parent Panel Access
**Role**: Parent
- **Username**: `parent`
- **Password**: `parent123`
- **Dashboard**: `/dashboard/parent/`

**Features**:
- Child's profile viewing
- Performance monitoring
- Attendance tracking
- Exam results viewing
- Mentor feedback access

---

### 5. 👔 Staff Panel Access
**Role**: College Staff
- **Username**: `staff` (Create new user)
- **Password**: `staff123`
- **Dashboard**: `/dashboard/staff/`

**Note**: Staff user needs to be created with role `college_staff`

**Features**:
- Students list with search/filters
- Student detail view
- Course-wise reports
- Attendance management
- Leave request approval
- Top performers viewing

---

## 🎯 Quick Access URLs

### Main Application
- **Homepage**: http://127.0.0.1:8000/
- **Login Page**: http://127.0.0.1:8000/login/
- **About Page**: http://127.0.0.1:8000/about/
- **Contact Page**: http://127.0.0.1:8000/contact/

### Admin Dashboards
- **Admin Dashboard**: http://127.0.0.1:8000/dashboard/admin/
- **Django Admin**: http://127.0.0.1:8000/admin/

### User Dashboards
- **Student Dashboard**: http://127.0.0.1:8000/dashboard/student/
- **Mentor Dashboard**: http://127.0.0.1:8000/dashboard/mentor/
- **Parent Dashboard**: http://127.0.0.1:8000/dashboard/parent/
- **Staff Dashboard**: http://127.0.0.1:8000/dashboard/staff/

### Special Features
- **Top Performers**: http://127.0.0.1:8000/dashboard/top-performers/
- **Mentor Approvals**: http://127.0.0.1:8000/dashboard/mentor/top-performers/

---

## 📱 Testing Guide

### 1. Admin Testing
1. Login with admin credentials
2. Go to Students section - Add/Edit/Delete students
3. Create courses and batches
4. Add mentors and assign students
5. Create exams and announcements

### 2. Student Testing
1. Login with student credentials
2. Check dashboard - see progress and rank
3. Go to Assignments - submit assignments
4. Take exams in Exams section
5. Mark attendance with GPS

### 3. Mentor Testing
1. Login with mentor credentials
2. View assigned students
3. Evaluate pending assignments
4. Approve top performers
5. Check attendance records

### 4. Parent Testing
1. Login with parent credentials
2. View child's profile
3. Check performance reports
4. Monitor attendance
5. See exam results

---

## 🏆 Top Performers Feature

### How to Test:
1. **Login as Admin** - Create TopPerformer entries in Django admin
2. **Login as Mentor** - Go to "Top Performers" and approve entries
3. **Login as Student** - See rank on dashboard if in top 5
4. **Login as Staff** - View top performers section

### Sample Data Creation:
```python
# In Django shell: python manage.py shell
from core.models import TopPerformer
from users.models import Student
from courses.models import Batch

# Create top performer
student = Student.objects.first()
batch = Batch.objects.first()

TopPerformer.objects.create(
    student=student,
    batch=batch,
    period='monthly',
    month=3,
    year=2026,
    rank=1,
    total_marks=950,
    percentage=95.0,
    is_approved=False
)
```

---

## 🛠️ Admin Panel Features

### Django Admin Access
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`

**Available Models**:
- Users (All roles)
- Students
- Courses, Phases, Modules, Topics
- Assignments & Submissions
- Exams & Attempts
- Attendance Records
- Top Performers
- Exam Schedules
- Leave Requests

---

## 📊 Sample Data

The system comes with pre-populated sample data:
- ✅ 4 Course Phases
- ✅ 20 Topics
- ✅ Sample assignments
- ✅ Attendance records
- ✅ User accounts for all roles

---

## 🔧 Troubleshooting

### If Login Fails:
1. Check if server is running: http://127.0.0.1:8000/
2. Try creating new superuser: `python manage.py createsuperuser`
3. Reset password in Django admin

### If Features Don't Work:
1. Run migrations: `python manage.py migrate`
2. Collect static files: `python manage.py collectstatic`
3. Check server logs in terminal

---

## 🎉 Ready to Use!

**Server Status**: ✅ Running on http://127.0.0.1:8000/

**All Panels**: ✅ Working
- Admin Panel ✅
- Student Panel ✅  
- Mentor Panel ✅
- Parent Panel ✅
- Staff Panel ✅

**New Features**: ✅ Implemented
- Top Performers System ✅
- Exam Schedules ✅
- Rank Display ✅
- Mentor Approvals ✅

---

**Happy Testing! 🚀**

Start with Admin login to explore all features, then test other roles!