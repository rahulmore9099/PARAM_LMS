# Smart LMS - Training Institute Learning Management System

A comprehensive Learning Management System built with Django, TailwindCSS, and Alpine.js for training institutes.

## Features

### 🎓 Core Modules
- **Multi-Role Authentication**: Admin, Student, Mentor, College Staff, Parent, HR, Accounts, Business Development
- **Course Management**: Hierarchical structure (Course → Phase → Module → Topic)
- **Phase Unlock System**: Mentor approval + Exam pass required
- **Built-in Code Compiler**: Support for Python, Java, C#, JavaScript, Go
- **Exam System**: MCQ, Practical Coding, Mock Interviews, Final Assessments
- **AI Doubt Assistant**: Powered by LLaMA/OpenAI/Groq
- **Real-time Chat**: Django Channels with WebSockets
- **Attendance System**: Daily, QR-based, Manual with leave requests
- **Assignment Management**: Code, File, GitHub link submissions
- **Progress Tracking**: Detailed student analytics and reports
- **Kit Tracking**: Laptop, IoT Kit, Books, ID Cards
- **Expert Sessions**: Live classes and recordings

### 🎨 UI/UX
- **Modern Design**: TailwindCSS with professional animations
- **Color Scheme**: 
  - Primary: #2563EB (Blue)
  - Secondary: #0F172A (Dark Navy)
  - Accent: #22C55E (Green)
  - Background: #F8FAFC
- **Responsive**: Mobile-first design
- **Interactive**: Alpine.js for dynamic components

## Tech Stack

- **Backend**: Python 3.x + Django 5.2.10
- **Frontend**: Django Templates + TailwindCSS + Alpine.js
- **Database**: PostgreSQL (SQLite for development)
- **Real-time**: Django Channels + Redis
- **Authentication**: Session-based + Role-based Authorization
- **File Storage**: AWS S3 / Local
- **AI**: OpenAI / Groq API
- **Reports**: Pandas + ReportLab

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite works for development)
- Redis (for WebSocket support)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd smart_lms
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## Project Structure

```
smart_lms/
├── smart_lms/          # Project settings
├── core/               # Core app (home, about, contact)
├── users/              # User management & authentication
├── courses/            # Course, Phase, Module, Topic management
├── exams/              # Exam and assessment system
├── attendance/         # Attendance tracking
├── chat/               # Real-time messaging
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
└── requirements.txt    # Python dependencies
```

## User Roles

1. **Admin**: Full system access
2. **Student**: Course access, assignments, exams
3. **Mentor**: Student management, evaluation
4. **College Staff**: College-specific student reports
5. **Parent**: View child's progress
6. **HR**: Employee management
7. **Accounts**: Financial management
8. **Business Development**: Lead management

## Key Features Detail

### Phase Unlock System
Students can only progress to the next phase when:
- ✅ Mentor approves
- ✅ Phase exam is passed
- ✅ All assignments submitted
- ✅ Practical work completed

### Built-in Code Compiler
- Docker sandboxed execution
- Support for multiple languages
- Test case validation
- Real-time code execution

### AI Doubt Assistant
- Trained on course content
- Instant doubt resolution
- Context-aware responses
- LangChain + RAG implementation

### Reports & Analytics
- Student progress reports
- Attendance reports
- Exam performance
- Batch analytics
- Export to Excel/PDF

## Database Models

### Main Models
- User, Student, Staff
- Course, Phase, Module, Topic
- Assignment, AssignmentSubmission
- Exam, Question, ExamAttempt
- Attendance, LeaveRequest
- ChatRoom, Message
- KitTracking, ExpertSession
- StudentProgress, StudentReport

## API Endpoints

The system uses Django REST Framework for API endpoints:
- `/api/courses/` - Course management
- `/api/students/` - Student operations
- `/api/exams/` - Exam system
- `/api/attendance/` - Attendance tracking
- `/api/chat/` - Messaging

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel
Access at `http://127.0.0.1:8000/admin/`

## Deployment

### Production Settings
1. Set `DEBUG=False` in .env
2. Configure PostgreSQL database
3. Set up Redis for channels
4. Configure AWS S3 for file storage
5. Set proper `ALLOWED_HOSTS`
6. Use gunicorn for WSGI
7. Set up Nginx as reverse proxy

### Using Gunicorn
```bash
gunicorn smart_lms.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email info@smartlms.com or join our Slack channel.

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Video conferencing integration
- [ ] Advanced analytics dashboard
- [ ] Gamification features
- [ ] Certificate generation
- [ ] Payment gateway integration
- [ ] Multi-language support

## Credits

Developed with ❤️ by Smart LMS Team

---

**Note**: This is a production-ready LMS system. Customize according to your institute's requirements.
