# Smart LMS - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup Script (Windows)
```bash
setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file
- Run database migrations
- Create superuser account
- Collect static files

### Step 2: Configure Environment (Optional)

Edit `.env` file for custom configuration:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL (optional)
DB_NAME=smart_lms_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Step 3: Start Development Server
```bash
python manage.py runserver
```

### Step 4: Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login Page**: http://127.0.0.1:8000/login/

## 📋 Default Pages Available

1. **Home** (`/`) - Landing page with features
2. **About** (`/about/`) - About the institute
3. **Contact** (`/contact/`) - Contact form
4. **Login** (`/login/`) - User authentication

## 👤 Creating Test Users

### Via Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Navigate to Users → Add User
4. Fill in details and select role:
   - Admin
   - Student
   - Mentor
   - College Staff
   - Parent
   - HR
   - Accounts
   - Business Development

### Via Django Shell

```bash
python manage.py shell
```

```python
from users.models import User, Student
from courses.models import Course, Batch

# Create a mentor
mentor = User.objects.create_user(
    username='mentor1',
    email='mentor@example.com',
    password='password123',
    role='mentor',
    first_name='John',
    last_name='Mentor'
)

# Create a student user
student_user = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='password123',
    role='student',
    first_name='Jane',
    last_name='Student'
)

# Create student profile
student = Student.objects.create(
    user=student_user,
    enrollment_number='ENR001',
    mentor=mentor
)
```

## 🎓 Setting Up Courses

### Via Admin Panel

1. Go to Admin → Courses → Add Course
2. Create a course (e.g., "Full Stack Python Django")
3. Add Phases to the course:
   - Phase 1: Python Basics
   - Phase 2: Django Framework
   - Phase 3: REST APIs
   - Phase 4: Deployment
4. Add Modules to each Phase
5. Add Topics to each Module
6. Create Batches and assign students

## 🎨 Customizing the Design

### Colors
Edit `templates/base.html` to change color scheme:
```javascript
colors: {
    primary: '#2563EB',    // Change primary color
    secondary: '#0F172A',  // Change secondary color
    accent: '#22C55E',     // Change accent color
}
```

### Logo
Replace the graduation cap icon in navigation with your logo:
```html
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## 📱 Features to Explore

### For Students
- View enrolled courses
- Track progress
- Submit assignments
- Take exams
- Chat with mentors
- AI doubt assistant

### For Mentors
- Manage students
- Evaluate assignments
- Create exams
- Track attendance
- Approve phase completion

### For Admin
- Full system control
- User management
- Course creation
- Reports and analytics
- System configuration

## 🔧 Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

## 🐛 Troubleshooting

### Database Issues
If using SQLite (default), the database file `db.sqlite3` will be created automatically.

For PostgreSQL:
1. Install PostgreSQL
2. Create database: `CREATE DATABASE smart_lms_db;`
3. Update .env with credentials
4. Run migrations

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Module Not Found Errors
```bash
pip install -r requirements.txt
```

## 📚 Next Steps

1. **Populate Sample Data**: Create courses, batches, and students
2. **Configure Email**: Set up SMTP for notifications
3. **Set up Redis**: For real-time chat functionality
4. **Configure AI**: Add OpenAI/Groq API keys for AI assistant
5. **Customize Templates**: Modify templates to match your branding

## 🎯 Production Deployment

For production deployment:
1. Set `DEBUG=False` in .env
2. Configure PostgreSQL
3. Set up Redis for channels
4. Configure AWS S3 for media files
5. Use gunicorn + nginx
6. Set up SSL certificate
7. Configure domain and DNS

## 💡 Tips

- Use the admin panel to quickly add test data
- Check the README.md for detailed documentation
- All models are registered in admin for easy management
- The system uses session-based authentication
- Role-based access control is built-in

## 🆘 Need Help?

- Check README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com/
- TailwindCSS docs: https://tailwindcss.com/docs
- Alpine.js docs: https://alpinejs.dev/

---

**Happy Learning! 🎓**
