# Admin CRUD Views for Smart LMS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta

from users.models import User, Student, Staff
from courses.models import Course, Phase, Module, Topic, Batch, Assignment, Announcement
from exams.models import Exam, Question
from attendance.models import Attendance, LeaveRequest

# ==================== STUDENTS CRUD ====================

@login_required
def students_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    students = Student.objects.select_related('user', 'course', 'batch', 'mentor').all()
    
    # Search
    search = request.GET.get('search')
    if search:
        students = students.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(enrollment_number__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    # Filters
    course_id = request.GET.get('course')
    if course_id:
        students = students.filter(course_id=course_id)
    
    batch_id = request.GET.get('batch')
    if batch_id:
        students = students.filter(batch_id=batch_id)
    
    status = request.GET.get('status')
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    
    # Stats
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    
    context = {
        'students': students,
        'courses': Course.objects.filter(is_active=True),
        'batches': Batch.objects.filter(is_active=True),
        'active_count': Student.objects.filter(is_active=True).count(),
        'inactive_count': Student.objects.filter(is_active=False).count(),
        'new_this_month': Student.objects.filter(admission_date__gte=thirty_days_ago).count(),
    }
    return render(request, 'dashboard/admin_students.html', context)


@login_required
def student_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Create user
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                role='student',
                phone=request.POST.get('phone', ''),
                date_of_birth=request.POST.get('date_of_birth') or None,
                address=request.POST.get('address', ''),
                is_verified=True
            )
            
            # Handle profile picture
            if request.FILES.get('profile_picture'):
                user.profile_picture = request.FILES['profile_picture']
                user.save()
            
            # Create student profile
            student = Student.objects.create(
                user=user,
                enrollment_number=request.POST.get('enrollment_number'),
                course_id=request.POST.get('course') or None,
                batch_id=request.POST.get('batch') or None,
                mentor_id=request.POST.get('mentor') or None,
                college_name=request.POST.get('college_name', ''),
                is_active=True
            )
            
            messages.success(request, f'Student {user.get_full_name()} added successfully!')
            return redirect('admin_students')
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    context = {
        'courses': Course.objects.filter(is_active=True),
        'batches': Batch.objects.filter(is_active=True),
        'mentors': User.objects.filter(role='mentor', is_active=True),
    }
    return render(request, 'dashboard/admin_add_student.html', context)


@login_required
def student_edit(request, student_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        try:
            # Update user
            user = student.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone', '')
            user.date_of_birth = request.POST.get('date_of_birth') or None
            user.address = request.POST.get('address', '')
            
            # Update password if provided
            new_password = request.POST.get('password')
            if new_password:
                user.set_password(new_password)
            
            # Handle profile picture
            if request.FILES.get('profile_picture'):
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            
            # Update student profile
            student.enrollment_number = request.POST.get('enrollment_number')
            student.course_id = request.POST.get('course') or None
            student.batch_id = request.POST.get('batch') or None
            student.mentor_id = request.POST.get('mentor') or None
            student.college_name = request.POST.get('college_name', '')
            student.save()
            
            messages.success(request, f'Student {user.get_full_name()} updated successfully!')
            return redirect('admin_students')
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    context = {
        'student': student,
        'courses': Course.objects.filter(is_active=True),
        'batches': Batch.objects.filter(is_active=True),
        'mentors': User.objects.filter(role='mentor', is_active=True),
    }
    return render(request, 'dashboard/admin_edit_student.html', context)


@login_required
def student_delete(request, student_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        user = student.user
        name = user.get_full_name()
        student.delete()
        user.delete()
        messages.success(request, f'Student {name} deleted successfully!')
        return redirect('admin_students')
    
    return render(request, 'dashboard/admin_delete_student.html', {'student': student})


@login_required
def student_view(request, student_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student.objects.select_related('user', 'course', 'batch', 'mentor'), id=student_id)
    
    context = {
        'student': student,
    }
    return render(request, 'dashboard/admin_view_student.html', context)


# ==================== COURSES CRUD ====================

@login_required
def courses_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    courses = Course.objects.all()
    
    # Search
    search = request.GET.get('search')
    if search:
        courses = courses.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    # Filter
    status = request.GET.get('status')
    if status == 'active':
        courses = courses.filter(is_active=True)
    elif status == 'inactive':
        courses = courses.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    
    context = {
        'courses': courses,
        'active_count': Course.objects.filter(is_active=True).count(),
        'inactive_count': Course.objects.filter(is_active=False).count(),
    }
    return render(request, 'dashboard/admin_courses.html', context)


@login_required
def course_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            course = Course.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                duration_months=request.POST.get('duration_months'),
                is_active=request.POST.get('is_active') == 'on'
            )
            
            if request.FILES.get('thumbnail'):
                course.thumbnail = request.FILES['thumbnail']
                course.save()
            
            messages.success(request, f'Course {course.name} added successfully!')
            return redirect('admin_courses')
        except Exception as e:
            messages.error(request, f'Error adding course: {str(e)}')
    
    return render(request, 'dashboard/admin_add_course.html')


@login_required
def course_edit(request, course_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        try:
            course.name = request.POST.get('name')
            course.description = request.POST.get('description')
            course.duration_months = request.POST.get('duration_months')
            course.is_active = request.POST.get('is_active') == 'on'
            
            if request.FILES.get('thumbnail'):
                course.thumbnail = request.FILES['thumbnail']
            
            course.save()
            
            messages.success(request, f'Course {course.name} updated successfully!')
            return redirect('admin_courses')
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
    
    context = {'course': course}
    return render(request, 'dashboard/admin_edit_course.html', context)


@login_required
def course_delete(request, course_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Course {name} deleted successfully!')
        return redirect('admin_courses')
    
    return render(request, 'dashboard/admin_delete_course.html', {'course': course})


# ==================== BATCHES CRUD ====================

@login_required
def batches_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    batches = Batch.objects.select_related('course', 'mentor').all()
    
    # Search
    search = request.GET.get('search')
    if search:
        batches = batches.filter(Q(name__icontains=search))
    
    # Pagination
    paginator = Paginator(batches, 10)
    page = request.GET.get('page')
    batches = paginator.get_page(page)
    
    context = {
        'batches': batches,
        'active_count': Batch.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/admin_batches.html', context)


@login_required
def batch_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            batch = Batch.objects.create(
                name=request.POST.get('name'),
                course_id=request.POST.get('course'),
                mentor_id=request.POST.get('mentor') or None,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                is_active=request.POST.get('is_active') == 'on'
            )
            
            messages.success(request, f'Batch {batch.name} added successfully!')
            return redirect('admin_batches')
        except Exception as e:
            messages.error(request, f'Error adding batch: {str(e)}')
    
    context = {
        'courses': Course.objects.filter(is_active=True),
        'mentors': User.objects.filter(role='mentor', is_active=True),
    }
    return render(request, 'dashboard/admin_add_batch.html', context)


@login_required
def batch_edit(request, batch_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    batch = get_object_or_404(Batch, id=batch_id)
    
    if request.method == 'POST':
        try:
            batch.name = request.POST.get('name')
            batch.course_id = request.POST.get('course')
            batch.mentor_id = request.POST.get('mentor') or None
            batch.start_date = request.POST.get('start_date')
            batch.end_date = request.POST.get('end_date')
            batch.is_active = request.POST.get('is_active') == 'on'
            batch.save()
            
            messages.success(request, f'Batch {batch.name} updated successfully!')
            return redirect('admin_batches')
        except Exception as e:
            messages.error(request, f'Error updating batch: {str(e)}')
    
    context = {
        'batch': batch,
        'courses': Course.objects.filter(is_active=True),
        'mentors': User.objects.filter(role='mentor', is_active=True),
    }
    return render(request, 'dashboard/admin_edit_batch.html', context)


@login_required
def batch_delete(request, batch_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    batch = get_object_or_404(Batch, id=batch_id)
    
    if request.method == 'POST':
        name = batch.name
        batch.delete()
        messages.success(request, f'Batch {name} deleted successfully!')
        return redirect('admin_batches')
    
    return render(request, 'dashboard/admin_delete_batch.html', {'batch': batch})


# ==================== EXAMS CRUD ====================

@login_required
def exams_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    exams = Exam.objects.select_related('phase').all()
    
    # Search
    search = request.GET.get('search')
    if search:
        exams = exams.filter(Q(title__icontains=search))
    
    # Pagination
    paginator = Paginator(exams, 10)
    page = request.GET.get('page')
    exams = paginator.get_page(page)
    
    context = {
        'exams': exams,
        'active_count': Exam.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/admin_exams.html', context)


@login_required
def exam_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            exam = Exam.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                exam_type=request.POST.get('exam_type'),
                phase_id=request.POST.get('phase'),
                duration_minutes=request.POST.get('duration_minutes'),
                total_marks=request.POST.get('total_marks'),
                pass_marks=request.POST.get('pass_marks'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                is_active=request.POST.get('is_active') == 'on'
            )
            
            messages.success(request, f'Exam {exam.title} added successfully!')
            return redirect('admin_exams')
        except Exception as e:
            messages.error(request, f'Error adding exam: {str(e)}')
    
    context = {
        'phases': Phase.objects.all(),
    }
    return render(request, 'dashboard/admin_add_exam.html', context)


# ==================== ANNOUNCEMENTS CRUD ====================

@login_required
def announcements_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    announcements = Announcement.objects.select_related('created_by', 'batch').all()
    
    # Pagination
    paginator = Paginator(announcements, 10)
    page = request.GET.get('page')
    announcements = paginator.get_page(page)
    
    context = {
        'announcements': announcements,
    }
    return render(request, 'dashboard/admin_announcements.html', context)


@login_required
def announcement_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            announcement = Announcement.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                created_by=request.user,
                batch_id=request.POST.get('batch') or None,
                is_important=request.POST.get('is_important') == 'on'
            )
            
            messages.success(request, f'Announcement "{announcement.title}" posted successfully!')
            return redirect('admin_announcements')
        except Exception as e:
            messages.error(request, f'Error posting announcement: {str(e)}')
    
    context = {
        'batches': Batch.objects.filter(is_active=True),
    }
    return render(request, 'dashboard/admin_add_announcement.html', context)


@login_required
def announcement_delete(request, announcement_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == 'POST':
        title = announcement.title
        announcement.delete()
        messages.success(request, f'Announcement "{title}" deleted successfully!')
        return redirect('admin_announcements')
    
    return render(request, 'dashboard/admin_delete_announcement.html', {'announcement': announcement})


# ==================== ATTENDANCE MANAGEMENT ====================

@login_required
def attendance_list(request):
    if request.user.role not in ['admin', 'staff', 'mentor']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    attendances = Attendance.objects.select_related('student__user', 'marked_by').all()
    
    # Filters
    date_filter = request.GET.get('date')
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    
    batch_id = request.GET.get('batch')
    if batch_id:
        attendances = attendances.filter(student__batch_id=batch_id)
    
    status = request.GET.get('status')
    if status:
        attendances = attendances.filter(status=status)
    
    # Pagination
    paginator = Paginator(attendances, 20)
    page = request.GET.get('page')
    attendances = paginator.get_page(page)
    
    # Stats
    today = datetime.now().date()
    context = {
        'attendances': attendances,
        'batches': Batch.objects.filter(is_active=True),
        'present_today': Attendance.objects.filter(date=today, status='present').count(),
        'absent_today': Attendance.objects.filter(date=today, status='absent').count(),
        'late_today': Attendance.objects.filter(date=today, status='late').count(),
    }
    return render(request, 'dashboard/admin_attendance.html', context)


@login_required
def attendance_mark(request):
    if request.user.role not in ['admin', 'staff', 'mentor']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            date = request.POST.get('date')
            status = request.POST.get('status')
            in_time = request.POST.get('in_time')
            out_time = request.POST.get('out_time')
            remarks = request.POST.get('remarks', '')
            
            # Location data
            in_latitude = request.POST.get('in_latitude')
            in_longitude = request.POST.get('in_longitude')
            in_location_address = request.POST.get('in_location_address', '')
            
            attendance, created = Attendance.objects.update_or_create(
                student_id=student_id,
                date=date,
                defaults={
                    'status': status,
                    'in_time': in_time if in_time else None,
                    'out_time': out_time if out_time else None,
                    'marked_by': request.user,
                    'remarks': remarks,
                    'in_latitude': in_latitude if in_latitude else None,
                    'in_longitude': in_longitude if in_longitude else None,
                    'in_location_address': in_location_address,
                }
            )
            
            action = 'marked' if created else 'updated'
            messages.success(request, f'Attendance {action} successfully!')
            return redirect('admin_attendance')
        except Exception as e:
            messages.error(request, f'Error marking attendance: {str(e)}')
    
    context = {
        'students': Student.objects.filter(is_active=True).select_related('user', 'batch'),
        'today': datetime.now().date(),
    }
    return render(request, 'dashboard/admin_mark_attendance.html', context)


@login_required
def attendance_calendar(request):
    if request.user.role not in ['admin', 'staff', 'mentor']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get month and year from request or use current
    from datetime import datetime
    import calendar
    
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Get first and last day of month
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    
    # Get attendance for the month
    attendances = Attendance.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).select_related('student__user')
    
    # Group by date
    attendance_by_date = {}
    for att in attendances:
        if att.date not in attendance_by_date:
            attendance_by_date[att.date] = {
                'present': 0,
                'absent': 0,
                'late': 0,
                'half_day': 0,
            }
        attendance_by_date[att.date][att.status] += 1
    
    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'attendance_by_date': attendance_by_date,
        'calendar_days': calendar.monthcalendar(year, month),
    }
    return render(request, 'dashboard/admin_attendance_calendar.html', context)


@login_required
def attendance_report(request):
    if request.user.role not in ['admin', 'staff', 'mentor']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get date range
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    batch_id = request.GET.get('batch')
    
    students = Student.objects.filter(is_active=True).select_related('user', 'batch')
    
    if batch_id:
        students = students.filter(batch_id=batch_id)
    
    # Calculate attendance stats for each student
    student_stats = []
    for student in students:
        attendances = student.attendances.all()
        
        if from_date:
            attendances = attendances.filter(date__gte=from_date)
        if to_date:
            attendances = attendances.filter(date__lte=to_date)
        
        total = attendances.count()
        present = attendances.filter(status='present').count()
        absent = attendances.filter(status='absent').count()
        late = attendances.filter(status='late').count()
        
        percentage = (present / total * 100) if total > 0 else 0
        
        student_stats.append({
            'student': student,
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'percentage': round(percentage, 2),
        })
    
    context = {
        'student_stats': student_stats,
        'batches': Batch.objects.filter(is_active=True),
        'from_date': from_date,
        'to_date': to_date,
        'batch_id': batch_id,
    }
    return render(request, 'dashboard/admin_attendance_report.html', context)


# ==================== MENTORS CRUD ====================

@login_required
def mentors_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    mentors = User.objects.filter(role='mentor')
    
    # Search
    search = request.GET.get('search')
    if search:
        mentors = mentors.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(mentors, 10)
    page = request.GET.get('page')
    mentors = paginator.get_page(page)
    
    context = {
        'mentors': mentors,
        'active_count': User.objects.filter(role='mentor', is_active=True).count(),
        'inactive_count': User.objects.filter(role='mentor', is_active=False).count(),
    }
    return render(request, 'dashboard/admin_mentors.html', context)


@login_required
def mentor_add(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                role='mentor',
                phone=request.POST.get('phone', ''),
                date_of_birth=request.POST.get('date_of_birth') or None,
                address=request.POST.get('address', ''),
                is_verified=True
            )
            
            if request.FILES.get('profile_picture'):
                user.profile_picture = request.FILES['profile_picture']
                user.save()
            
            messages.success(request, f'Mentor {user.get_full_name()} added successfully!')
            return redirect('admin_mentors')
        except Exception as e:
            messages.error(request, f'Error adding mentor: {str(e)}')
    
    return render(request, 'dashboard/admin_add_mentor.html')


@login_required
def mentor_edit(request, mentor_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    mentor = get_object_or_404(User, id=mentor_id, role='mentor')
    
    if request.method == 'POST':
        try:
            mentor.first_name = request.POST.get('first_name')
            mentor.last_name = request.POST.get('last_name')
            mentor.email = request.POST.get('email')
            mentor.phone = request.POST.get('phone', '')
            mentor.date_of_birth = request.POST.get('date_of_birth') or None
            mentor.address = request.POST.get('address', '')
            
            new_password = request.POST.get('password')
            if new_password:
                mentor.set_password(new_password)
            
            if request.FILES.get('profile_picture'):
                mentor.profile_picture = request.FILES['profile_picture']
            
            mentor.save()
            
            messages.success(request, f'Mentor {mentor.get_full_name()} updated successfully!')
            return redirect('admin_mentors')
        except Exception as e:
            messages.error(request, f'Error updating mentor: {str(e)}')
    
    context = {'mentor': mentor}
    return render(request, 'dashboard/admin_edit_mentor.html', context)


@login_required
def mentor_delete(request, mentor_id):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    mentor = get_object_or_404(User, id=mentor_id, role='mentor')
    
    if request.method == 'POST':
        name = mentor.get_full_name()
        mentor.delete()
        messages.success(request, f'Mentor {name} deleted successfully!')
        return redirect('admin_mentors')
    
    return render(request, 'dashboard/admin_delete_mentor.html', {'mentor': mentor})
