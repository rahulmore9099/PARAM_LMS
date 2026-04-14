from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math


# ---------------------------------------------------------------------------
# GPS helpers
# ---------------------------------------------------------------------------

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Returns great-circle distance in metres between two GPS coordinate pairs."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def determine_attendance_status(distance_m: float, radius_m: float) -> str:
    """Returns 'present' if within radius, else 'absent'."""
    return 'present' if distance_m <= radius_m else 'absent'


# ---------------------------------------------------------------------------
# Registration helpers
# ---------------------------------------------------------------------------

def is_valid_phone(phone: str) -> bool:
    """Returns True iff phone is exactly 10 ASCII digits."""
    return phone.isdigit() and len(phone) == 10


def validate_registration_data(data: dict) -> dict:
    """
    Validates registration POST data.
    Returns dict of field_name -> [error_messages]. Empty dict means all valid.
    """
    from users.models import User
    errors = {}

    required = ['full_name', 'email', 'phone', 'parent_phone', 'parent_name',
                'residence_type', 'technology', 'password', 'confirm_password']
    for field in required:
        if not data.get(field, '').strip():
            errors.setdefault(field, []).append('This field is required.')

    email = data.get('email', '').strip()
    if email and User.objects.filter(email=email).exists():
        errors.setdefault('email', []).append('An account with this email already exists.')

    phone = data.get('phone', '').strip()
    if phone and not is_valid_phone(phone):
        errors.setdefault('phone', []).append('Mobile number must be exactly 10 digits.')

    parent_phone = data.get('parent_phone', '').strip()
    if parent_phone and not is_valid_phone(parent_phone):
        errors.setdefault('parent_phone', []).append("Parent's mobile number must be exactly 10 digits.")

    password = data.get('password', '')
    if password and len(password) < 8:
        errors.setdefault('password', []).append('Password must be at least 8 characters.')

    confirm = data.get('confirm_password', '')
    if password and confirm and password != confirm:
        errors.setdefault('confirm_password', []).append('Passwords do not match.')

    return errors

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course = request.POST.get('course')
        message = request.POST.get('message')
        
        # Here you can save to database or send email
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        from users.models import User
        login_input = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Support both username and email login
        user_obj = User.objects.filter(email=login_input).first()
        if not user_obj:
            user_obj = User.objects.filter(username=login_input).first()

        user = None
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please check your username/email and password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def register_view(request):
    """Student self-registration."""
    from users.models import User, Student
    from courses.models import Course

    mentors = User.objects.filter(role='mentor', is_active=True)
    courses = Course.objects.filter(is_active=True)

    if request.method == 'POST':
        data = {
            'full_name': request.POST.get('full_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'parent_phone': request.POST.get('parent_phone', '').strip(),
            'parent_name': request.POST.get('parent_name', '').strip(),
            'residence_type': request.POST.get('residence_type', '').strip(),
            'technology': request.POST.get('technology', '').strip(),
            'mentor_id': request.POST.get('mentor_id', '').strip(),
            'password': request.POST.get('password', ''),
            'confirm_password': request.POST.get('confirm_password', ''),
        }

        errors = validate_registration_data(data)

        if errors:
            return render(request, 'register.html', {
                'errors': errors,
                'post': data,
                'mentors': mentors,
                'courses': courses,
            })

        # Build username from email prefix, ensure uniqueness
        base_username = data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        name_parts = data['full_name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=data['email'],
            password=data['password'],
            first_name=first_name,
            last_name=last_name,
            role='student',
            phone=data['phone'],
            is_verified=True,
        )

        # Generate enrollment number
        enrollment_number = f"PARAM{User.objects.count():05d}"

        mentor = None
        if data['mentor_id']:
            mentor = User.objects.filter(id=data['mentor_id'], role='mentor').first()

        course = Course.objects.filter(id=data['technology']).first()

        Student.objects.create(
            user=user,
            enrollment_number=enrollment_number,
            course=course,
            mentor=mentor,
            parent_name=data['parent_name'],
            residence_type=data['residence_type'],
            is_active=True,
        )

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html', {
        'mentors': mentors,
        'courses': courses,
    })

@login_required
def dashboard(request):
    user = request.user
    
    # Redirect based on user role
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'mentor':
        return redirect('mentor_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'college_staff':
        return redirect('staff_dashboard')
    elif user.role == 'parent':
        return redirect('parent_dashboard')
    else:
        return render(request, 'dashboard/base_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')

    from users.models import Student, User
    from courses.models import Course, Batch, AssignmentSubmission
    from exams.models import Exam
    from attendance.models import Attendance
    from datetime import date, datetime

    today = date.today()
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Attendance today
    total_today = Attendance.objects.filter(date=today).count()
    present_today = Attendance.objects.filter(date=today, status='present').count()
    attendance_today = int((present_today / total_today * 100)) if total_today > 0 else 0

    # Pending assignments
    pending_assignments = AssignmentSubmission.objects.filter(status='submitted').count()

    # Upcoming exams (active, not yet ended)
    upcoming_exams = Exam.objects.filter(is_active=True, end_time__gte=datetime.now()).count()

    context = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_mentors': User.objects.filter(role='mentor', is_active=True).count(),
        'total_courses': Course.objects.filter(is_active=True).count(),
        'total_batches': Batch.objects.filter(is_active=True).count(),
        'active_students': Student.objects.filter(is_active=True).count(),
        'pending_approvals': Student.objects.filter(is_active=False).count(),
        'completed_courses': Course.objects.filter(is_active=False).count(),
        'upcoming_exams': upcoming_exams,
        'pending_assignments': pending_assignments,
        'attendance_today': attendance_today,
        'recent_students': Student.objects.select_related('user').order_by('-admission_date')[:5],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def admin_mentors(request):
    messages.info(request, 'Mentors management coming soon!')
    return redirect('admin_dashboard')

@login_required
def admin_attendance(request):
    messages.info(request, 'Attendance management coming soon!')
    return redirect('admin_dashboard')

@login_required
def admin_reports(request):
    messages.info(request, 'Reports coming soon!')
    return redirect('admin_dashboard')

@login_required
def admin_settings(request):
    messages.info(request, 'Settings coming soon!')
    return redirect('admin_dashboard')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import StudentProgress, AssignmentSubmission
    from attendance.models import Attendance
    from exams.models import ExamAttempt
    from datetime import date, datetime
    from django.db.models import Avg
    
    # Calculate statistics
    total_topics = 0
    completed_topics = 0
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                total_topics += module.topics.count()
        completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
    
    course_progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
    
    # Pending assignments
    pending_assignments = AssignmentSubmission.objects.filter(
        student=student, 
        status='pending'
    ).count()
    
    # Attendance percentage
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    # My rank in batch (current month) - with error handling
    my_rank = None
    upcoming_exams = []
    recent_results = []
    
    try:
        from core.models import TopPerformer, ExamSchedule
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        if student.batch:
            my_performance = TopPerformer.objects.filter(
                student=student,
                batch=student.batch,
                month=current_month,
                year=current_year,
                is_approved=True
            ).first()
            if my_performance:
                my_rank = my_performance.rank
        
        # Upcoming exams
        if student.batch:
            upcoming_exams = ExamSchedule.objects.filter(
                batch=student.batch,
                scheduled_date__gte=datetime.now(),
                is_announced=True
            ).select_related('exam').order_by('scheduled_date')[:3]
    except Exception as e:
        # If tables don't exist yet, just skip these features
        pass
    
    # Recent exam results
    recent_results = ExamAttempt.objects.filter(
        student=student,
        status='evaluated'
    ).select_related('exam').order_by('-start_time')[:3]

    # Phase-wise progress for dashboard
    phases_progress = []
    if student.course:
        for phase in student.course.phases.all():
            phase_topics = 0
            phase_completed = 0
            for module in phase.modules.all():
                for topic in module.topics.all():
                    phase_topics += 1
                    from courses.models import StudentProgress as SP
                    if SP.objects.filter(student=student, topic=topic, is_completed=True).exists():
                        phase_completed += 1
            phase_pct = int((phase_completed / phase_topics * 100)) if phase_topics > 0 else 0
            is_current = student.current_phase and student.current_phase.id == phase.id
            phases_progress.append({
                'phase': phase,
                'progress': phase_pct,
                'completed': phase_completed,
                'total': phase_topics,
                'is_current': is_current,
            })

    # Pending assignments for display
    from courses.models import Assignment, AssignmentSubmission as AS
    pending_assignments_list = []
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                for topic in module.topics.all():
                    for assignment in topic.assignments.all():
                        sub = AS.objects.filter(student=student, assignment=assignment).first()
                        if not sub or sub.status in ('pending', 'resubmit'):
                            pending_assignments_list.append({'assignment': assignment, 'submission': sub})
    pending_assignments_list = pending_assignments_list[:5]

    # Recent evaluated assignments
    recent_grades = AS.objects.filter(
        student=student, status='evaluated'
    ).select_related('assignment').order_by('-evaluated_at')[:5]

    context = {
        'student': student,
        'course_progress': course_progress,
        'completed_topics': completed_topics,
        'pending_assignments': pending_assignments,
        'attendance_percentage': attendance_percentage,
        'my_rank': my_rank,
        'upcoming_exams': upcoming_exams,
        'recent_results': recent_results,
        'phases_progress': phases_progress,
        'pending_assignments_list': pending_assignments_list,
        'recent_grades': recent_grades,
    }
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def student_courses(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import StudentProgress
    
    course = student.course
    if not course:
        messages.warning(request, 'No course assigned yet.')
        return redirect('student_dashboard')
    
    # Get all phases with progress
    phases_data = []
    for phase in course.phases.all():
        total_topics = 0
        completed_topics = 0
        
        modules_data = []
        for module in phase.modules.all():
            topics_data = []
            for topic in module.topics.all():
                total_topics += 1
                progress = StudentProgress.objects.filter(student=student, topic=topic).first()
                is_completed = progress.is_completed if progress else False
                if is_completed:
                    completed_topics += 1
                
                topics_data.append({
                    'topic': topic,
                    'is_completed': is_completed,
                    'progress': progress
                })
            
            modules_data.append({
                'module': module,
                'topics': topics_data
            })
        
        phase_progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
        is_unlocked = phase.order == 0 or (student.current_phase and phase.order <= student.current_phase.order)
        
        phases_data.append({
            'phase': phase,
            'modules': modules_data,
            'progress': phase_progress,
            'is_unlocked': is_unlocked,
            'total_topics': total_topics,
            'completed_topics': completed_topics
        })
    
    context = {
        'student': student,
        'course': course,
        'phases_data': phases_data,
    }
    return render(request, 'dashboard/student_curriculum.html', context)

@login_required
def student_assignments(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import Assignment, AssignmentSubmission
    from django.db.models import Q
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Get all assignments for student's course
    assignments = []
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                for topic in module.topics.all():
                    for assignment in topic.assignments.all():
                        submission = AssignmentSubmission.objects.filter(
                            student=student, 
                            assignment=assignment
                        ).first()
                        
                        assignments.append({
                            'assignment': assignment,
                            'submission': submission,
                            'phase': phase,
                            'module': module,
                            'topic': topic
                        })
    
    # Apply filter
    if status_filter == 'pending':
        assignments = [a for a in assignments if not a['submission']]
    elif status_filter == 'submitted':
        assignments = [a for a in assignments if a['submission'] and a['submission'].status == 'submitted']
    elif status_filter == 'evaluated':
        assignments = [a for a in assignments if a['submission'] and a['submission'].status == 'evaluated']
    
    context = {
        'student': student,
        'assignments': assignments,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/student_assignments.html', context)

@login_required
def submit_assignment(request, assignment_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import Assignment, AssignmentSubmission
    from django.shortcuts import get_object_or_404
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = AssignmentSubmission.objects.filter(student=student, assignment=assignment).first()
    
    if request.method == 'POST':
        submission_text = request.POST.get('submission_text', '')
        github_link = request.POST.get('github_link', '')
        file = request.FILES.get('file')
        
        if submission:
            submission.submission_text = submission_text
            submission.github_link = github_link
            if file:
                submission.file = file
            submission.status = 'submitted'
            submission.save()
            messages.success(request, 'Assignment resubmitted successfully!')
        else:
            submission = AssignmentSubmission.objects.create(
                assignment=assignment,
                student=student,
                submission_text=submission_text,
                github_link=github_link,
                file=file,
                status='submitted'
            )
            messages.success(request, 'Assignment submitted successfully!')
        
        return redirect('student_assignments')
    
    context = {
        'student': student,
        'assignment': assignment,
        'submission': submission,
    }
    return render(request, 'dashboard/student_submit_assignment.html', context)

@login_required
def student_exams(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from exams.models import Exam, ExamAttempt
    from datetime import datetime
    
    # Get all exams for student's course
    exams_data = []
    if student.course:
        for phase in student.course.phases.all():
            for exam in phase.exams.filter(is_active=True):
                attempt = ExamAttempt.objects.filter(student=student, exam=exam).first()
                
                exams_data.append({
                    'exam': exam,
                    'phase': phase,
                    'attempt': attempt,
                    'can_attempt': datetime.now() >= exam.start_time.replace(tzinfo=None) and datetime.now() <= exam.end_time.replace(tzinfo=None)
                })
    
    context = {
        'student': student,
        'exams_data': exams_data,
    }
    return render(request, 'dashboard/student_exams.html', context)

@login_required
def take_exam(request, exam_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from exams.models import Exam, ExamAttempt, Answer
    from django.shortcuts import get_object_or_404
    from datetime import datetime
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if exam is available
    now = datetime.now()
    if now < exam.start_time.replace(tzinfo=None) or now > exam.end_time.replace(tzinfo=None):
        messages.error(request, 'This exam is not available at this time.')
        return redirect('student_exams')
    
    # Get or create attempt
    attempt = ExamAttempt.objects.filter(student=student, exam=exam).first()
    
    if request.method == 'POST':
        if not attempt:
            attempt = ExamAttempt.objects.create(student=student, exam=exam, status='in_progress')
        
        # Save answers
        for question in exam.questions.all():
            answer_text = request.POST.get(f'question_{question.id}', '')
            selected_option = request.POST.get(f'mcq_{question.id}', '')
            
            Answer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    'answer_text': answer_text,
                    'selected_option': selected_option,
                }
            )
        
        # Mark as submitted
        attempt.status = 'submitted'
        attempt.end_time = datetime.now()
        attempt.save()
        
        messages.success(request, 'Exam submitted successfully!')
        return redirect('student_exams')
    
    if not attempt:
        attempt = ExamAttempt.objects.create(student=student, exam=exam, status='in_progress')
    
    context = {
        'student': student,
        'exam': exam,
        'attempt': attempt,
        'questions': exam.questions.all(),
    }
    return render(request, 'dashboard/student_take_exam.html', context)

@login_required
def student_attendance(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from attendance.models import Attendance
    from datetime import date, timedelta
    from django.db.models import Count, Q
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    
    # Calculate statistics
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    absent_days = attendance_records.filter(status='absent').count()
    leave_days = attendance_records.filter(status='leave').count()
    
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    # Get current month data for calendar
    today = date.today()
    first_day = today.replace(day=1)
    
    context = {
        'student': student,
        'attendance_records': attendance_records[:30],  # Last 30 records
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'dashboard/student_attendance.html', context)

@login_required
def mark_my_attendance(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')

    try:
        student = request.user.student_profile
    except Exception:
        messages.error(request, 'Student profile not found.')
        return redirect('home')

    from attendance.models import Attendance
    from datetime import date
    from django.conf import settings

    today_attendance = Attendance.objects.filter(student=student, date=date.today()).first()

    if request.method == 'POST':
        # Duplicate check
        if today_attendance:
            messages.warning(request, 'Attendance already marked for today.')
            return redirect('student_attendance')

        lat_str = request.POST.get('lat', '').strip()
        lon_str = request.POST.get('lon', '').strip()

        if not lat_str or not lon_str:
            messages.error(request, 'Location access is required to mark attendance.')
            return redirect('mark_my_attendance')

        try:
            lat = float(lat_str)
            lon = float(lon_str)
        except ValueError:
            messages.error(request, 'Invalid location data received.')
            return redirect('mark_my_attendance')

        inst_lat = getattr(settings, 'INSTITUTE_LATITUDE', 0.0)
        inst_lon = getattr(settings, 'INSTITUTE_LONGITUDE', 0.0)
        radius = getattr(settings, 'INSTITUTE_RADIUS_METERS', 200)

        distance = haversine_distance(lat, lon, inst_lat, inst_lon)
        status = determine_attendance_status(distance, radius)

        from datetime import datetime
        in_time = datetime.now().time()

        Attendance.objects.create(
            student=student,
            date=date.today(),
            status=status,
            in_time=in_time,
            in_latitude=lat,
            in_longitude=lon,
            in_location_address=request.POST.get('location_address', ''),
            marked_by=request.user,
        )

        if status == 'present':
            messages.success(request, f'Attendance marked as Present. You are within the institute premises.')
        else:
            messages.warning(request, f'Attendance marked as Absent. Your location is {int(distance)}m from the institute (allowed: {radius}m).')

        return redirect('student_attendance')

    context = {
        'student': student,
        'today_attendance': today_attendance,
    }
    return render(request, 'dashboard/student_mark_attendance.html', context)

@login_required
def student_progress(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import StudentProgress, AssignmentSubmission
    from exams.models import ExamAttempt
    from attendance.models import Attendance
    
    # Overall progress
    total_topics = 0
    completed_topics = 0
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                total_topics += module.topics.count()
        completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
    
    overall_progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
    
    # Phase-wise progress
    phases_progress = []
    if student.course:
        for phase in student.course.phases.all():
            phase_topics = 0
            phase_completed = 0
            for module in phase.modules.all():
                for topic in module.topics.all():
                    phase_topics += 1
                    progress = StudentProgress.objects.filter(student=student, topic=topic, is_completed=True).first()
                    if progress:
                        phase_completed += 1
            
            phase_progress = int((phase_completed / phase_topics * 100)) if phase_topics > 0 else 0
            phases_progress.append({
                'phase': phase,
                'progress': phase_progress,
                'completed': phase_completed,
                'total': phase_topics
            })
    
    # Assignments stats
    total_assignments = AssignmentSubmission.objects.filter(student=student).count()
    submitted_assignments = AssignmentSubmission.objects.filter(student=student, status__in=['submitted', 'evaluated']).count()
    
    # Exams stats
    total_exams = ExamAttempt.objects.filter(student=student).count()
    passed_exams = ExamAttempt.objects.filter(student=student, is_passed=True).count()
    
    # Attendance stats
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    context = {
        'student': student,
        'overall_progress': overall_progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'phases_progress': phases_progress,
        'total_assignments': total_assignments,
        'submitted_assignments': submitted_assignments,
        'total_exams': total_exams,
        'passed_exams': passed_exams,
        'attendance_percentage': attendance_percentage,
        'present_days': present_days,
        'total_days': total_days,
    }
    return render(request, 'dashboard/student_progress.html', context)

@login_required
def student_explanation(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import Topic, StudentProgress
    
    # Get all topics with videos
    topics_with_videos = []
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                for topic in module.topics.all():
                    progress = StudentProgress.objects.filter(student=student, topic=topic).first()
                    topics_with_videos.append({
                        'topic': topic,
                        'phase': phase,
                        'module': module,
                        'is_completed': progress.is_completed if progress else False,
                        'is_unlocked': phase.order == 0 or (student.current_phase and phase.order <= student.current_phase.order)
                    })
    
    context = {
        'student': student,
        'topics_with_videos': topics_with_videos,
    }
    return render(request, 'dashboard/student_explanation.html', context)

@login_required
def watch_video(request, topic_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from courses.models import Topic, StudentProgress
    from django.shortcuts import get_object_or_404
    
    topic = get_object_or_404(Topic, id=topic_id)
    progress = StudentProgress.objects.filter(student=student, topic=topic).first()
    
    # Mark as in progress if not already completed
    if not progress:
        progress = StudentProgress.objects.create(student=student, topic=topic, is_completed=False)
    
    context = {
        'student': student,
        'topic': topic,
        'progress': progress,
    }
    return render(request, 'dashboard/student_watch_video.html', context)

@login_required
def student_project(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')

    try:
        student = request.user.student_profile
    except Exception:
        messages.error(request, 'Student profile not found.')
        return redirect('home')

    from core.models import ProjectMember
    memberships = ProjectMember.objects.filter(student=student).select_related('project__mentor')

    context = {
        'student': student,
        'memberships': memberships,
    }
    return render(request, 'dashboard/student_project.html', context)


@login_required
def student_ai_help(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    from core.models import AIDoubt
    
    # Get conversation history
    conversations = AIDoubt.objects.filter(student=student).order_by('-created_at')[:20]
    
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        
        if question:
            # Simple AI response (can be replaced with actual AI API)
            answer = generate_ai_response(question)
            
            # Save conversation
            AIDoubt.objects.create(
                student=student,
                question=question,
                answer=answer
            )
            
            messages.success(request, 'Question answered!')
            return redirect('student_ai_help')
    
    context = {
        'student': student,
        'conversations': conversations,
    }
    return render(request, 'dashboard/student_ai_help.html', context)

def generate_ai_response(question):
    """
    Simple AI response generator
    Can be replaced with OpenAI API or other AI service
    """
    question_lower = question.lower()
    
    # Simple keyword-based responses
    if 'python' in question_lower:
        return "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation. Would you like to know more about a specific Python topic?"
    
    elif 'django' in question_lower:
        return "Django is a high-level Python web framework that encourages rapid development and clean design. It follows the MVT (Model-View-Template) pattern and includes features like ORM, authentication, and admin interface out of the box."
    
    elif 'function' in question_lower:
        return "Functions in Python are defined using the 'def' keyword. They help organize code into reusable blocks. Example:\n\ndef greet(name):\n    return f'Hello, {name}!'\n\nWould you like to learn more about function parameters or return values?"
    
    elif 'variable' in question_lower:
        return "Variables in Python are used to store data. You don't need to declare their type explicitly. Example:\n\nname = 'John'\nage = 25\nis_student = True\n\nPython automatically determines the data type based on the value assigned."
    
    elif 'loop' in question_lower or 'for' in question_lower or 'while' in question_lower:
        return "Python has two main types of loops:\n\n1. for loop - iterates over a sequence\nfor i in range(5):\n    print(i)\n\n2. while loop - repeats while condition is true\nwhile x < 10:\n    x += 1\n\nWhich type would you like to explore further?"
    
    elif 'class' in question_lower or 'oop' in question_lower:
        return "Classes in Python are blueprints for creating objects. They support Object-Oriented Programming (OOP) concepts like inheritance, encapsulation, and polymorphism. Example:\n\nclass Student:\n    def __init__(self, name):\n        self.name = name\n    \n    def study(self):\n        print(f'{self.name} is studying')"
    
    elif 'error' in question_lower or 'debug' in question_lower:
        return "Common debugging tips:\n\n1. Read error messages carefully\n2. Use print() statements to check variable values\n3. Check for typos in variable/function names\n4. Verify indentation (Python is sensitive to it)\n5. Use try-except blocks for error handling\n\nWhat specific error are you encountering?"
    
    elif 'help' in question_lower or 'how' in question_lower:
        return "I'm here to help! You can ask me about:\n\n• Python basics (variables, functions, loops)\n• Django framework\n• Data structures\n• Debugging tips\n• Code examples\n• Concept explanations\n\nWhat would you like to learn about?"
    
    else:
        return f"That's an interesting question about '{question}'. Let me help you understand this better.\n\nCould you provide more context or specify which aspect you'd like to focus on? For example:\n\n• Are you looking for a code example?\n• Do you need an explanation of a concept?\n• Are you facing a specific error?\n\nFeel free to ask more specific questions, and I'll provide detailed answers!"

@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')

    from users.models import Student
    from courses.models import AssignmentSubmission, StudentProgress
    from exams.models import ExamAttempt
    from attendance.models import Attendance
    from datetime import datetime, date

    my_students = Student.objects.filter(mentor=request.user, is_active=True)

    pending_assignments = AssignmentSubmission.objects.filter(
        student__mentor=request.user, status='submitted'
    ).count()

    pending_exams = ExamAttempt.objects.filter(
        student__mentor=request.user, status='submitted'
    ).count()

    pending_approvals = 0
    try:
        from core.models import TopPerformer
        current_month = datetime.now().month
        current_year = datetime.now().year
        pending_approvals = TopPerformer.objects.filter(
            student__mentor=request.user,
            is_approved=False,
            month=current_month,
            year=current_year
        ).count()
    except Exception:
        pass

    # Real attendance today for mentor's students
    today = date.today()
    student_ids = my_students.values_list('id', flat=True)
    total_today = Attendance.objects.filter(student_id__in=student_ids, date=today).count()
    present_today = Attendance.objects.filter(student_id__in=student_ids, date=today, status='present').count()
    attendance_today = int((present_today / total_today * 100)) if total_today > 0 else 0

    # Recent pending submissions for display
    recent_pending = AssignmentSubmission.objects.filter(
        student__mentor=request.user, status='submitted'
    ).select_related('student__user', 'assignment').order_by('-submitted_at')[:5]

    # Students with progress
    students_data = []
    for student in my_students.select_related('user', 'course', 'batch')[:5]:
        total_topics = 0
        completed_topics = 0
        if student.course:
            for phase in student.course.phases.all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
        progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
        students_data.append({'student': student, 'progress': progress})

    context = {
        'total_students': my_students.count(),
        'pending_assignments': pending_assignments,
        'pending_exams': pending_exams,
        'pending_evaluations': pending_assignments + pending_exams,
        'pending_approvals': pending_approvals,
        'upcoming_sessions': 0,
        'attendance_today': attendance_today,
        'recent_students': my_students.select_related('user')[:5],
        'recent_pending': recent_pending,
        'students_data': students_data,
    }
    return render(request, 'dashboard/mentor_dashboard.html', context)

@login_required
def mentor_students(request):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from users.models import Student
    from courses.models import StudentProgress
    
    # Get all students assigned to this mentor
    students = Student.objects.filter(mentor=request.user, is_active=True).select_related('user', 'course', 'batch')
    
    # Calculate progress for each student
    students_data = []
    for student in students:
        total_topics = 0
        completed_topics = 0
        
        if student.course:
            for phase in student.course.phases.all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
        
        progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
        
        students_data.append({
            'student': student,
            'progress': progress,
            'completed_topics': completed_topics,
            'total_topics': total_topics
        })
    
    context = {
        'students_data': students_data,
    }
    return render(request, 'dashboard/mentor_students.html', context)

@login_required
def mentor_evaluations(request):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from courses.models import AssignmentSubmission
    from exams.models import ExamAttempt
    
    # Get pending assignments
    pending_assignments = AssignmentSubmission.objects.filter(
        student__mentor=request.user,
        status='submitted'
    ).select_related('student__user', 'assignment__topic')
    
    # Get pending exams
    pending_exams = ExamAttempt.objects.filter(
        student__mentor=request.user,
        status='submitted'
    ).select_related('student__user', 'exam')
    
    context = {
        'pending_assignments': pending_assignments,
        'pending_exams': pending_exams,
    }
    return render(request, 'dashboard/mentor_evaluations.html', context)

@login_required
def evaluate_assignment(request, submission_id):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from courses.models import AssignmentSubmission
    from django.shortcuts import get_object_or_404
    from datetime import datetime
    
    submission = get_object_or_404(AssignmentSubmission, id=submission_id, student__mentor=request.user)
    
    if request.method == 'POST':
        marks = request.POST.get('marks')
        feedback = request.POST.get('feedback')
        status = request.POST.get('status', 'evaluated')
        
        submission.marks_obtained = int(marks) if marks else None
        submission.feedback = feedback
        submission.status = status
        submission.evaluated_by = request.user
        submission.evaluated_at = datetime.now()
        submission.save()
        
        messages.success(request, 'Assignment evaluated successfully!')
        return redirect('mentor_evaluations')
    
    context = {
        'submission': submission,
    }
    return render(request, 'dashboard/mentor_evaluate_assignment.html', context)

@login_required
def mentor_attendance(request):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from attendance.models import Attendance
    from datetime import date
    
    # Get today's attendance for mentor's students
    today = date.today()
    attendance_records = Attendance.objects.filter(
        student__mentor=request.user,
        date=today
    ).select_related('student__user')
    
    # Get all students
    from users.models import Student
    all_students = Student.objects.filter(mentor=request.user, is_active=True)
    
    context = {
        'attendance_records': attendance_records,
        'all_students': all_students,
        'today': today,
    }
    return render(request, 'dashboard/mentor_attendance.html', context)


@login_required
def mentor_update_student_phase(request, student_id):
    if request.user.role != 'mentor':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Access denied. Mentors only.')

    if request.method != 'POST':
        return redirect('mentor_students')

    from users.models import Student
    from courses.models import Phase
    from django.shortcuts import get_object_or_404

    student = get_object_or_404(Student, id=student_id, mentor=request.user)
    phase_id = request.POST.get('phase_id')
    phase = get_object_or_404(Phase, id=phase_id)

    student.current_phase = phase
    student.save()
    messages.success(request, f'Phase updated to "{phase.name}" for {student.user.get_full_name()}.')
    return redirect('mentor_students')


@login_required
def mentor_projects(request):
    if request.user.role != 'mentor':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Access denied. Mentors only.')

    from core.models import Project, ProjectMember
    from users.models import Student

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        progress = int(request.POST.get('progress_percentage', 0))
        member_ids = request.POST.getlist('members')

        if title and description:
            project = Project.objects.create(
                title=title,
                description=description,
                mentor=request.user,
                progress_percentage=max(0, min(100, progress)),
            )
            for sid in member_ids:
                student = Student.objects.filter(id=sid).first()
                if student:
                    ProjectMember.objects.get_or_create(project=project, student=student)
            messages.success(request, f'Project "{project.title}" created successfully!')
        else:
            messages.error(request, 'Title and description are required.')
        return redirect('mentor_projects')

    projects = Project.objects.filter(mentor=request.user).prefetch_related('members__student__user')
    students = Student.objects.filter(mentor=request.user, is_active=True).select_related('user')

    context = {
        'projects': projects,
        'students': students,
    }
    return render(request, 'dashboard/mentor_projects.html', context)


@login_required
def mentor_project_detail(request, project_id):
    if request.user.role != 'mentor':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Access denied. Mentors only.')

    from core.models import Project, ProjectMember
    from users.models import Student
    from django.shortcuts import get_object_or_404

    project = get_object_or_404(Project, id=project_id, mentor=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_progress':
            progress = int(request.POST.get('progress_percentage', project.progress_percentage))
            project.progress_percentage = max(0, min(100, progress))
            project.save()
            messages.success(request, 'Project progress updated.')

        elif action == 'add_member':
            student_id = request.POST.get('student_id')
            student = Student.objects.filter(id=student_id).first()
            if student:
                ProjectMember.objects.get_or_create(project=project, student=student)
                messages.success(request, f'{student.user.get_full_name()} added to project.')

        elif action == 'remove_member':
            student_id = request.POST.get('student_id')
            ProjectMember.objects.filter(project=project, student_id=student_id).delete()
            messages.success(request, 'Member removed from project.')

        return redirect('mentor_project_detail', project_id=project.id)

    current_member_ids = project.members.values_list('student_id', flat=True)
    available_students = Student.objects.filter(
        mentor=request.user, is_active=True
    ).exclude(id__in=current_member_ids).select_related('user')

    context = {
        'project': project,
        'available_students': available_students,
    }
    return render(request, 'dashboard/mentor_project_detail.html', context)


@login_required
def staff_dashboard(request):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')

    from users.models import Student
    from courses.models import StudentProgress
    from attendance.models import Attendance, LeaveRequest
    from datetime import datetime, date

    # Scope: staff sees students from their college (via Staff profile) or all if no college set
    college_name = ''
    try:
        college_name = request.user.staff_profile.college_name
    except Exception:
        pass

    students_qs = Student.objects.filter(is_active=True).select_related('user', 'course', 'batch', 'mentor')
    if college_name:
        students_qs = students_qs.filter(college_name=college_name)

    total_students = students_qs.count()

    # Pending leave requests scoped to these students
    student_ids = students_qs.values_list('id', flat=True)
    pending_leaves = LeaveRequest.objects.filter(student_id__in=student_ids, status='pending').count()

    # Average attendance for scoped students
    attendance_qs = Attendance.objects.filter(student_id__in=student_ids)
    total_attendance = attendance_qs.count()
    present_records = attendance_qs.filter(status='present').count()
    avg_attendance = int((present_records / total_attendance * 100)) if total_attendance > 0 else 0

    # Average performance (topic completion %)
    total_progress = 0
    for student in students_qs:
        total_topics = 0
        completed_topics = 0
        if student.course:
            for phase in student.course.phases.prefetch_related('modules__topics').all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
        progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
        total_progress += progress

    avg_performance = int(total_progress / total_students) if total_students > 0 else 0

    # Top performers this month
    top_performers = []
    try:
        from core.models import TopPerformer
        current_month = datetime.now().month
        current_year = datetime.now().year
        top_performers = TopPerformer.objects.filter(
            student_id__in=student_ids,
            month=current_month,
            year=current_year,
            is_approved=True
        ).select_related('student__user', 'batch').order_by('batch', 'rank')[:10]
    except Exception:
        pass

    # Recent students with stats
    recent_students = students_qs.order_by('-admission_date')[:10]
    students_data = []
    for student in recent_students:
        total_topics = 0
        completed_topics = 0
        if student.course:
            for phase in student.course.phases.all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
        progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0

        total_days = Attendance.objects.filter(student=student).count()
        present_days = Attendance.objects.filter(student=student, status='present').count()
        attendance = int((present_days / total_days * 100)) if total_days > 0 else 0

        student_rank = None
        try:
            from core.models import TopPerformer
            student_rank = TopPerformer.objects.filter(
                student=student,
                month=datetime.now().month,
                year=datetime.now().year,
                is_approved=True
            ).first()
        except Exception:
            pass

        students_data.append({
            'student': student,
            'progress': progress,
            'attendance': attendance,
            'rank': student_rank.rank if student_rank else None,
        })

    context = {
        'total_students': total_students,
        'pending_leaves': pending_leaves,
        'avg_attendance': avg_attendance,
        'avg_performance': avg_performance,
        'students_data': students_data,
        'top_performers': top_performers,
        'college_name': college_name,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        messages.error(request, 'Access denied. Parents only.')
        return redirect('dashboard')
    
    from users.models import Student
    from courses.models import StudentProgress, AssignmentSubmission
    from attendance.models import Attendance
    from exams.models import ExamAttempt
    
    # Get parent's children
    children = Student.objects.filter(parent=request.user, is_active=True)
    
    if not children.exists():
        context = {'children': children}
        return render(request, 'dashboard/parent_dashboard.html', context)
    
    # Get first child's data for dashboard
    child = children.first()
    
    # Calculate progress
    total_topics = 0
    completed_topics = 0
    if child.course:
        for phase in child.course.phases.all():
            for module in phase.modules.all():
                total_topics += module.topics.count()
        completed_topics = StudentProgress.objects.filter(student=child, is_completed=True).count()
    
    progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
    
    # Attendance
    total_days = Attendance.objects.filter(student=child).count()
    present_days = Attendance.objects.filter(student=child, status='present').count()
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    # Assignments
    pending_assignments = AssignmentSubmission.objects.filter(student=child, status='pending').count()
    
    # Exams
    recent_exams = ExamAttempt.objects.filter(student=child).order_by('-start_time')[:3]
    
    context = {
        'children': children,
        'child': child,
        'progress': progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'attendance_percentage': attendance_percentage,
        'present_days': present_days,
        'total_days': total_days,
        'pending_assignments': pending_assignments,
        'recent_exams': recent_exams,
    }
    return render(request, 'dashboard/parent_dashboard.html', context)

@login_required
def parent_child_profile(request, student_id=None):
    if request.user.role != 'parent':
        messages.error(request, 'Access denied. Parents only.')
        return redirect('dashboard')
    
    from users.models import Student
    from courses.models import StudentProgress
    from django.shortcuts import get_object_or_404
    
    if student_id:
        child = get_object_or_404(Student, id=student_id, parent=request.user)
    else:
        child = Student.objects.filter(parent=request.user, is_active=True).first()
        if not child:
            messages.warning(request, 'No child profile found.')
            return redirect('parent_dashboard')
    
    # Calculate progress
    total_topics = 0
    completed_topics = 0
    if child.course:
        for phase in child.course.phases.all():
            for module in phase.modules.all():
                total_topics += module.topics.count()
        completed_topics = StudentProgress.objects.filter(student=child, is_completed=True).count()
    
    progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
    
    context = {
        'child': child,
        'progress': progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
    }
    return render(request, 'dashboard/parent_child_profile.html', context)

@login_required
def parent_performance(request, student_id=None):
    if request.user.role != 'parent':
        messages.error(request, 'Access denied. Parents only.')
        return redirect('dashboard')
    
    from users.models import Student
    from courses.models import StudentProgress, AssignmentSubmission
    from exams.models import ExamAttempt
    from django.shortcuts import get_object_or_404
    
    if student_id:
        child = get_object_or_404(Student, id=student_id, parent=request.user)
    else:
        child = Student.objects.filter(parent=request.user, is_active=True).first()
        if not child:
            messages.warning(request, 'No child profile found.')
            return redirect('parent_dashboard')
    
    # Phase-wise progress
    phases_progress = []
    if child.course:
        for phase in child.course.phases.all():
            phase_topics = 0
            phase_completed = 0
            for module in phase.modules.all():
                for topic in module.topics.all():
                    phase_topics += 1
                    progress = StudentProgress.objects.filter(student=child, topic=topic, is_completed=True).first()
                    if progress:
                        phase_completed += 1
            
            phase_progress = int((phase_completed / phase_topics * 100)) if phase_topics > 0 else 0
            phases_progress.append({
                'phase': phase,
                'progress': phase_progress,
                'completed': phase_completed,
                'total': phase_topics
            })
    
    # Assignments
    assignments = AssignmentSubmission.objects.filter(student=child).select_related('assignment').order_by('-submitted_at')[:10]
    
    # Exams
    exams = ExamAttempt.objects.filter(student=child).select_related('exam').order_by('-start_time')[:10]
    
    context = {
        'child': child,
        'phases_progress': phases_progress,
        'assignments': assignments,
        'exams': exams,
    }
    return render(request, 'dashboard/parent_performance.html', context)

@login_required
def parent_attendance(request, student_id=None):
    if request.user.role != 'parent':
        messages.error(request, 'Access denied. Parents only.')
        return redirect('dashboard')
    
    from users.models import Student
    from attendance.models import Attendance
    from django.shortcuts import get_object_or_404
    
    if student_id:
        child = get_object_or_404(Student, id=student_id, parent=request.user)
    else:
        child = Student.objects.filter(parent=request.user, is_active=True).first()
        if not child:
            messages.warning(request, 'No child profile found.')
            return redirect('parent_dashboard')
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(student=child).order_by('-date')[:30]
    
    # Calculate statistics
    total_days = Attendance.objects.filter(student=child).count()
    present_days = Attendance.objects.filter(student=child, status='present').count()
    absent_days = Attendance.objects.filter(student=child, status='absent').count()
    leave_days = Attendance.objects.filter(student=child, status='leave').count()
    
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    context = {
        'child': child,
        'attendance_records': attendance_records,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'dashboard/parent_attendance.html', context)

@login_required
def parent_exams(request, student_id=None):
    if request.user.role != 'parent':
        messages.error(request, 'Access denied. Parents only.')
        return redirect('dashboard')
    
    from users.models import Student
    from exams.models import ExamAttempt
    from django.shortcuts import get_object_or_404
    
    if student_id:
        child = get_object_or_404(Student, id=student_id, parent=request.user)
    else:
        child = Student.objects.filter(parent=request.user, is_active=True).first()
        if not child:
            messages.warning(request, 'No child profile found.')
            return redirect('parent_dashboard')
    
    # Get exam attempts
    exam_attempts = ExamAttempt.objects.filter(student=child).select_related('exam').order_by('-start_time')
    
    # Calculate statistics
    total_exams = exam_attempts.count()
    passed_exams = exam_attempts.filter(is_passed=True).count()
    
    context = {
        'child': child,
        'exam_attempts': exam_attempts,
        'total_exams': total_exams,
        'passed_exams': passed_exams,
    }
    return render(request, 'dashboard/parent_exams.html', context)

# Staff Panel Views

@login_required
def staff_students(request):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')

    from users.models import Student
    from courses.models import StudentProgress, Course, Batch
    from attendance.models import Attendance
    from django.db.models import Q

    search = request.GET.get('search', '')
    course_filter = request.GET.get('course', '')
    batch_filter = request.GET.get('batch', '')

    # Scope by college
    college_name = ''
    try:
        college_name = request.user.staff_profile.college_name
    except Exception:
        pass

    students = Student.objects.filter(is_active=True).select_related('user', 'course', 'batch', 'mentor')
    if college_name:
        students = students.filter(college_name=college_name)

    if search:
        students = students.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(enrollment_number__icontains=search)
        )
    if course_filter:
        students = students.filter(course_id=course_filter)
    if batch_filter:
        students = students.filter(batch_id=batch_filter)

    students_data = []
    for student in students:
        total_topics = 0
        completed_topics = 0
        if student.course:
            for phase in student.course.phases.all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
        progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0

        total_days = Attendance.objects.filter(student=student).count()
        present_days = Attendance.objects.filter(student=student, status='present').count()
        attendance = int((present_days / total_days * 100)) if total_days > 0 else 0

        students_data.append({'student': student, 'progress': progress, 'attendance': attendance})

    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)

    context = {
        'students_data': students_data,
        'courses': courses,
        'batches': batches,
        'search': search,
        'course_filter': course_filter,
        'batch_filter': batch_filter,
    }
    return render(request, 'dashboard/staff_students.html', context)

@login_required
def staff_student_detail(request, student_id):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')
    
    from users.models import Student
    from courses.models import StudentProgress, AssignmentSubmission
    from attendance.models import Attendance
    from exams.models import ExamAttempt
    from django.shortcuts import get_object_or_404
    
    student = get_object_or_404(Student, id=student_id)
    
    # Progress
    total_topics = 0
    completed_topics = 0
    if student.course:
        for phase in student.course.phases.all():
            for module in phase.modules.all():
                total_topics += module.topics.count()
        completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
    
    progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
    
    # Attendance
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_percentage = int((present_days / total_days * 100)) if total_days > 0 else 0
    
    # Recent attendance
    recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
    
    # Assignments
    assignments = AssignmentSubmission.objects.filter(student=student).select_related('assignment').order_by('-submitted_at')[:5]
    
    # Exams
    exams = ExamAttempt.objects.filter(student=student).select_related('exam').order_by('-start_time')[:5]
    
    context = {
        'student': student,
        'progress': progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'attendance_percentage': attendance_percentage,
        'present_days': present_days,
        'total_days': total_days,
        'recent_attendance': recent_attendance,
        'assignments': assignments,
        'exams': exams,
    }
    return render(request, 'dashboard/staff_student_detail.html', context)

@login_required
def staff_reports(request):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')

    from users.models import Student
    from courses.models import Course, StudentProgress
    from attendance.models import Attendance

    # Scope by college
    college_name = ''
    try:
        college_name = request.user.staff_profile.college_name
    except Exception:
        pass

    students_qs = Student.objects.filter(is_active=True)
    if college_name:
        students_qs = students_qs.filter(college_name=college_name)

    total_students = students_qs.count()
    student_ids = students_qs.values_list('id', flat=True)

    # Overall attendance
    attendance_qs = Attendance.objects.filter(student_id__in=student_ids)
    total_att = attendance_qs.count()
    present_att = attendance_qs.filter(status='present').count()
    overall_attendance = int((present_att / total_att * 100)) if total_att > 0 else 0

    # Course-wise stats (only courses that have students in scope)
    course_ids = students_qs.values_list('course_id', flat=True).distinct()
    courses = Course.objects.filter(id__in=course_ids, is_active=True)
    course_stats = []
    for course in courses:
        course_students = students_qs.filter(course=course)
        student_count = course_students.count()

        course_att = Attendance.objects.filter(student__in=course_students)
        total_course_att = course_att.count()
        present_course = course_att.filter(status='present').count()
        avg_attendance = int((present_course / total_course_att * 100)) if total_course_att > 0 else 0

        total_progress = 0
        for student in course_students:
            total_topics = 0
            completed_topics = 0
            for phase in course.phases.all():
                for module in phase.modules.all():
                    total_topics += module.topics.count()
            completed_topics = StudentProgress.objects.filter(student=student, is_completed=True).count()
            progress = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
            total_progress += progress

        avg_progress = int(total_progress / student_count) if student_count > 0 else 0

        course_stats.append({
            'course': course,
            'student_count': student_count,
            'avg_attendance': avg_attendance,
            'avg_progress': avg_progress,
        })

    context = {
        'total_students': total_students,
        'overall_attendance': overall_attendance,
        'course_stats': course_stats,
    }
    return render(request, 'dashboard/staff_reports.html', context)

@login_required
def staff_attendance(request):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')

    from attendance.models import Attendance
    from users.models import Student
    from datetime import date

    selected_date = request.GET.get('date', str(date.today()))
    try:
        filter_date = date.fromisoformat(selected_date)
    except ValueError:
        filter_date = date.today()

    # Scope by college
    college_name = ''
    try:
        college_name = request.user.staff_profile.college_name
    except Exception:
        pass

    student_ids = Student.objects.filter(is_active=True)
    if college_name:
        student_ids = student_ids.filter(college_name=college_name)
    student_ids = student_ids.values_list('id', flat=True)

    attendance_records = Attendance.objects.filter(
        date=filter_date,
        student_id__in=student_ids
    ).select_related('student__user', 'student__course', 'student__batch').order_by('student__user__first_name')

    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    leave_count = attendance_records.filter(status='leave').count()

    context = {
        'attendance_records': attendance_records,
        'selected_date': filter_date,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
    }
    return render(request, 'dashboard/staff_attendance.html', context)

@login_required
def staff_leave_requests(request):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')

    from attendance.models import LeaveRequest
    from users.models import Student

    status_filter = request.GET.get('status', 'pending')

    college_name = ''
    try:
        college_name = request.user.staff_profile.college_name
    except Exception:
        pass

    student_ids = Student.objects.filter(is_active=True)
    if college_name:
        student_ids = student_ids.filter(college_name=college_name)
    student_ids = student_ids.values_list('id', flat=True)

    leave_requests = LeaveRequest.objects.filter(
        student_id__in=student_ids
    ).select_related('student__user', 'approved_by').order_by('-created_at')

    if status_filter != 'all':
        leave_requests = leave_requests.filter(status=status_filter)

    context = {
        'leave_requests': leave_requests,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/staff_leave_requests.html', context)

@login_required
def staff_approve_leave(request, leave_id):
    if request.user.role != 'college_staff':
        messages.error(request, 'Access denied. Staff only.')
        return redirect('dashboard')
    
    from attendance.models import LeaveRequest
    from django.shortcuts import get_object_or_404
    from datetime import datetime
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        if action == 'approve':
            leave_request.status = 'approved'
            leave_request.approved_by = request.user
            leave_request.remarks = remarks
            leave_request.save()
            messages.success(request, 'Leave request approved successfully!')
        elif action == 'reject':
            leave_request.status = 'rejected'
            leave_request.approved_by = request.user
            leave_request.remarks = remarks
            leave_request.save()
            messages.success(request, 'Leave request rejected.')
        
        return redirect('staff_leave_requests')
    
    context = {
        'leave_request': leave_request,
    }
    return render(request, 'dashboard/staff_approve_leave.html', context)


# Top Performers Management

@login_required
def mentor_top_performers(request):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from core.models import TopPerformer
    from datetime import datetime
    
    # Get filter
    status_filter = request.GET.get('status', 'pending')
    
    # Get top performers for mentor's students
    performers = TopPerformer.objects.filter(
        student__mentor=request.user
    ).select_related('student__user', 'batch').order_by('-year', '-month', 'rank')
    
    if status_filter == 'pending':
        performers = performers.filter(is_approved=False)
    elif status_filter == 'approved':
        performers = performers.filter(is_approved=True)
    
    context = {
        'performers': performers,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/mentor_top_performers.html', context)

@login_required
def mentor_approve_performer(request, performer_id):
    if request.user.role != 'mentor':
        messages.error(request, 'Access denied. Mentors only.')
        return redirect('dashboard')
    
    from core.models import TopPerformer
    from django.shortcuts import get_object_or_404
    from datetime import datetime
    
    performer = get_object_or_404(TopPerformer, id=performer_id, student__mentor=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        if action == 'approve':
            performer.is_approved = True
            performer.approved_by = request.user
            performer.approved_at = datetime.now()
            performer.remarks = remarks
            performer.save()
            messages.success(request, f'{performer.student.user.get_full_name()} approved as Rank {performer.rank} performer!')
        elif action == 'reject':
            performer.delete()
            messages.success(request, 'Top performer entry rejected and removed.')
        
        return redirect('mentor_top_performers')
    
    context = {
        'performer': performer,
    }
    return render(request, 'dashboard/mentor_approve_performer.html', context)

@login_required
def view_top_performers(request):
    """View for all users to see top performers"""
    from core.models import TopPerformer
    from datetime import datetime
    from courses.models import Batch
    
    # Get filters
    month = request.GET.get('month', str(datetime.now().month))
    year = request.GET.get('year', str(datetime.now().year))
    batch_id = request.GET.get('batch', '')
    
    # Get top performers
    performers = TopPerformer.objects.filter(
        month=int(month),
        year=int(year),
        is_approved=True
    ).select_related('student__user', 'batch').order_by('batch', 'rank')
    
    if batch_id:
        performers = performers.filter(batch_id=batch_id)
    
    # Group by batch
    batches_data = {}
    for performer in performers:
        batch_name = performer.batch.name
        if batch_name not in batches_data:
            batches_data[batch_name] = []
        batches_data[batch_name].append(performer)
    
    # Get all batches for filter
    batches = Batch.objects.filter(is_active=True)
    
    context = {
        'batches_data': batches_data,
        'batches': batches,
        'selected_month': int(month),
        'selected_year': int(year),
        'selected_batch': batch_id,
    }
    return render(request, 'dashboard/view_top_performers.html', context)
