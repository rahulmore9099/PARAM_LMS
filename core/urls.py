from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin Dashboard
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Students CRUD
    path('dashboard/admin/students/', admin_views.students_list, name='admin_students'),
    path('dashboard/admin/students/add/', admin_views.student_add, name='admin_add_student'),
    path('dashboard/admin/students/edit/<int:student_id>/', admin_views.student_edit, name='admin_edit_student'),
    path('dashboard/admin/students/delete/<int:student_id>/', admin_views.student_delete, name='admin_delete_student'),
    path('dashboard/admin/students/view/<int:student_id>/', admin_views.student_view, name='admin_view_student'),
    
    # Courses CRUD
    path('dashboard/admin/courses/', admin_views.courses_list, name='admin_courses'),
    path('dashboard/admin/courses/add/', admin_views.course_add, name='admin_add_course'),
    path('dashboard/admin/courses/edit/<int:course_id>/', admin_views.course_edit, name='admin_edit_course'),
    path('dashboard/admin/courses/delete/<int:course_id>/', admin_views.course_delete, name='admin_delete_course'),
    
    # Batches CRUD
    path('dashboard/admin/batches/', admin_views.batches_list, name='admin_batches'),
    path('dashboard/admin/batches/add/', admin_views.batch_add, name='admin_add_batch'),
    path('dashboard/admin/batches/edit/<int:batch_id>/', admin_views.batch_edit, name='admin_edit_batch'),
    path('dashboard/admin/batches/delete/<int:batch_id>/', admin_views.batch_delete, name='admin_delete_batch'),
    
    # Exams CRUD
    path('dashboard/admin/exams/', admin_views.exams_list, name='admin_exams'),
    path('dashboard/admin/exams/add/', admin_views.exam_add, name='admin_add_exam'),
    
    # Announcements CRUD
    path('dashboard/admin/announcements/', admin_views.announcements_list, name='admin_announcements'),
    path('dashboard/admin/announcements/add/', admin_views.announcement_add, name='admin_add_announcement'),
    path('dashboard/admin/announcements/delete/<int:announcement_id>/', admin_views.announcement_delete, name='admin_delete_announcement'),
    
    # Mentors CRUD
    path('dashboard/admin/mentors/', admin_views.mentors_list, name='admin_mentors'),
    path('dashboard/admin/mentors/add/', admin_views.mentor_add, name='admin_add_mentor'),
    path('dashboard/admin/mentors/edit/<int:mentor_id>/', admin_views.mentor_edit, name='admin_edit_mentor'),
    path('dashboard/admin/mentors/delete/<int:mentor_id>/', admin_views.mentor_delete, name='admin_delete_mentor'),
    
    # Attendance Management
    path('dashboard/admin/attendance/', admin_views.attendance_list, name='admin_attendance'),
    path('dashboard/admin/attendance/mark/', admin_views.attendance_mark, name='admin_mark_attendance'),
    path('dashboard/admin/attendance/calendar/', admin_views.attendance_calendar, name='admin_attendance_calendar'),
    path('dashboard/admin/attendance/report/', admin_views.attendance_report, name='admin_attendance_report'),
    
    # Other Admin Pages
    path('dashboard/admin/reports/', views.admin_reports, name='admin_reports'),
    path('dashboard/admin/settings/', views.admin_settings, name='admin_settings'),
    
    # Other Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/mentor/', views.mentor_dashboard, name='mentor_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    
    # Student Panel
    path('dashboard/student/courses/', views.student_courses, name='student_courses'),
    path('dashboard/student/explanation/', views.student_explanation, name='student_explanation'),
    path('dashboard/student/explanation/watch/<int:topic_id>/', views.watch_video, name='watch_video'),
    path('dashboard/student/ai-help/', views.student_ai_help, name='student_ai_help'),
    path('dashboard/student/assignments/', views.student_assignments, name='student_assignments'),
    path('dashboard/student/assignments/submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('dashboard/student/exams/', views.student_exams, name='student_exams'),
    path('dashboard/student/exams/take/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('dashboard/student/attendance/', views.student_attendance, name='student_attendance'),
    path('dashboard/student/attendance/mark/', views.mark_my_attendance, name='mark_my_attendance'),
    path('dashboard/student/progress/', views.student_progress, name='student_progress'),
    path('dashboard/student/project/', views.student_project, name='student_project'),
    
    # Mentor Panel
    path('dashboard/mentor/students/', views.mentor_students, name='mentor_students'),
    path('dashboard/mentor/evaluations/', views.mentor_evaluations, name='mentor_evaluations'),
    path('dashboard/mentor/evaluations/assignment/<int:submission_id>/', views.evaluate_assignment, name='evaluate_assignment'),
    path('dashboard/mentor/attendance/', views.mentor_attendance, name='mentor_attendance'),
    path('dashboard/mentor/top-performers/', views.mentor_top_performers, name='mentor_top_performers'),
    path('dashboard/mentor/top-performers/<int:performer_id>/', views.mentor_approve_performer, name='mentor_approve_performer'),
    path('dashboard/mentor/projects/', views.mentor_projects, name='mentor_projects'),
    path('dashboard/mentor/projects/<int:project_id>/', views.mentor_project_detail, name='mentor_project_detail'),
    path('dashboard/mentor/students/<int:student_id>/phase/', views.mentor_update_student_phase, name='mentor_update_student_phase'),
    
    # Top Performers (All users)
    path('dashboard/top-performers/', views.view_top_performers, name='view_top_performers'),
    
    # Parent Panel
    path('dashboard/parent/child/<int:student_id>/', views.parent_child_profile, name='parent_child_profile'),
    path('dashboard/parent/performance/<int:student_id>/', views.parent_performance, name='parent_performance'),
    path('dashboard/parent/attendance/<int:student_id>/', views.parent_attendance, name='parent_attendance'),
    path('dashboard/parent/exams/<int:student_id>/', views.parent_exams, name='parent_exams'),
    
    # Staff Panel
    path('dashboard/staff/students/', views.staff_students, name='staff_students'),
    path('dashboard/staff/students/<int:student_id>/', views.staff_student_detail, name='staff_student_detail'),
    path('dashboard/staff/reports/', views.staff_reports, name='staff_reports'),
    path('dashboard/staff/attendance/', views.staff_attendance, name='staff_attendance'),
    path('dashboard/staff/leave-requests/', views.staff_leave_requests, name='staff_leave_requests'),
    path('dashboard/staff/leave-requests/<int:leave_id>/', views.staff_approve_leave, name='staff_approve_leave'),
]
