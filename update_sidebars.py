"""
Script to update all student template sidebars to be consistent
"""

sidebar_menu = '''{% block sidebar_menu %}
<div class="space-y-1 px-3">
    <a href="{% url 'student_dashboard' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-home text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Dashboard</span>
    </a>
    
    <a href="{% url 'student_courses' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-book-open text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Curriculum</span>
    </a>
    
    <a href="#" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg" onclick="alert('Video explanations coming soon!'); return false;">
        <i class="fas fa-play-circle text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Explanation</span>
    </a>
    
    <a href="#" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg" onclick="alert('AI Help feature coming soon!'); return false;">
        <i class="fas fa-robot text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">AI Help</span>
    </a>
    
    <a href="{% url 'student_assignments' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-tasks text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Assignments</span>
    </a>
    
    <a href="{% url 'student_attendance' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-calendar-alt text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Attendance</span>
    </a>
    
    <a href="{% url 'student_progress' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-chart-line text-xl" :class="sidebarOpen ? '' : 'mx-auto'"></i>
        <span x-show="sidebarOpen">Progress</span>
    </a>
</div>
{% endblock %}'''

mobile_sidebar_menu = '''{% block mobile_sidebar_menu %}
<div class="space-y-1 px-3">
    <a href="{% url 'student_dashboard' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-home text-xl"></i><span>Dashboard</span>
    </a>
    <a href="{% url 'student_courses' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-book-open text-xl"></i><span>Curriculum</span>
    </a>
    <a href="#" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg" onclick="alert('Video explanations coming soon!'); return false;">
        <i class="fas fa-play-circle text-xl"></i><span>Explanation</span>
    </a>
    <a href="#" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg" onclick="alert('AI Help feature coming soon!'); return false;">
        <i class="fas fa-robot text-xl"></i><span>AI Help</span>
    </a>
    <a href="{% url 'student_assignments' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-tasks text-xl"></i><span>Assignments</span>
    </a>
    <a href="{% url 'student_attendance' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-calendar-alt text-xl"></i><span>Attendance</span>
    </a>
    <a href="{% url 'student_progress' %}" class="sidebar-link flex items-center space-x-3 px-4 py-3 rounded-lg">
        <i class="fas fa-chart-line text-xl"></i><span>Progress</span>
    </a>
</div>
{% endblock %}'''

print("Sidebar templates ready!")
print("\nUse these in all student templates:")
print("- student_assignments.html")
print("- student_submit_assignment.html")
print("- student_exams.html")
print("- student_take_exam.html")
print("- student_attendance.html")
print("- student_mark_attendance.html")
print("- student_progress.html")
