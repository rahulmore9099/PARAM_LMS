# Testing Guide - Student Panel

## Setup Complete ✅

All student panel features are now fully functional with sample data.

## Test Credentials

**Student Login:**
- Username: `student`
- Password: `student123`
- Enrollment: STU2024001

## What's Been Populated

### 1. Course Structure
- **Course:** Full Stack Python Django
- **Phases:** 4 phases (Phase 0-3)
- **Current Phase:** Phase 0 (Unlocked)
- **Modules:** 1 module in Phase 0
- **Topics:** 5 topics in the module

### 2. Topics Created
1. ✅ What is Machine Learning? (COMPLETED)
2. Three Types of Machine Learning
3. ML Workflow: Data → Model → Prediction
4. Setting up Python Environment
5. Quiz: Module 1 Assessment

### 3. Assignments
- Python Basics Assignment (Due in 7 days)
- Functions and Modules Project (Due in 14 days)

### 4. Exams
- Phase 0 Final Assessment (MCQ)
- 2 sample questions created
- Duration: 60 minutes
- Total Marks: 100
- Pass Marks: 70

### 5. Attendance
- 10 attendance records created
- 8 Present days
- 2 Absent days
- Attendance Percentage: 80%
- GPS locations included for present days

## Testing Steps

### 1. Login
```
http://127.0.0.1:8000/login/
Username: student
Password: student123
```

### 2. Test Dashboard
- Navigate to: http://127.0.0.1:8000/dashboard/student/
- Check statistics cards (should show real data)
- Verify progress percentages

### 3. Test Curriculum
- Click "My Courses" in sidebar
- URL: http://127.0.0.1:8000/dashboard/student/courses/
- Should see:
  - Phase 0 (Unlocked with 20% progress)
  - Phase 1-3 (Locked)
  - 5 topics listed
  - 1 topic marked as completed (green checkmark)
  - Start/Review buttons on topics

### 4. Test Assignments
- Click "Assignments" in sidebar
- URL: http://127.0.0.1:8000/dashboard/student/assignments/
- Should see 2 assignments
- Click "Submit Now" to test submission form
- Test filters: All, Pending, Submitted, Graded

### 5. Test Exams
- Click "Exams" in sidebar
- URL: http://127.0.0.1:8000/dashboard/student/exams/
- Should see Phase 0 Final Assessment
- Click "Start Exam" to test exam interface
- Timer should start counting down
- 2 MCQ questions should appear

### 6. Test Attendance
- Click "Attendance" in sidebar
- URL: http://127.0.0.1:8000/dashboard/student/attendance/
- Should see:
  - Statistics: 8 Present, 2 Absent, 80%
  - 10 attendance records in table
  - GPS locations for present days
- Click "Mark Attendance" button
- Test GPS location capture (allow browser location access)

### 7. Test Progress
- Click "Progress" in sidebar
- URL: http://127.0.0.1:8000/dashboard/student/progress/
- Should see:
  - Overall progress circle (20%)
  - Phase-wise progress bars
  - Learning activity metrics
  - Attendance overview
  - Achievement badges

## Expected Behavior

### Curriculum Page
- ✅ Phase 0 shows as "Unlocked" (green badge)
- ✅ Phase 1-3 show as "Locked" (gray badge)
- ✅ Progress bar shows 20% (1 of 5 topics completed)
- ✅ First topic has green checkmark and "Review" button
- ✅ Other topics have "Start" button
- ✅ Locked phases show lock icon and requirements

### Assignments Page
- ✅ 2 assignments listed
- ✅ Both show "Not Submitted" status (red badge)
- ✅ "Submit Now" button available
- ✅ Due dates displayed
- ✅ Max marks shown

### Exams Page
- ✅ 1 exam listed (Phase 0 Final Assessment)
- ✅ "Start Exam" button available
- ✅ Exam details: 60 mins, 100 marks, Pass: 70

### Attendance Page
- ✅ Statistics cards show correct numbers
- ✅ Table shows 10 records
- ✅ GPS locations visible for present days
- ✅ "Mark Attendance" button works

### Progress Page
- ✅ Overall progress: 20%
- ✅ Topics completed: 1/5
- ✅ Assignments: 0/2 submitted
- ✅ Exams: 0/1 attempted
- ✅ Attendance: 80%

## Mobile Responsiveness

Test on different screen sizes:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

All pages should:
- ✅ Sidebar collapses on mobile
- ✅ Cards stack vertically
- ✅ Tables become scrollable
- ✅ Buttons remain accessible
- ✅ Forms are touch-friendly

## Common Issues & Solutions

### Issue: No data showing
**Solution:** Run `python populate_student_data.py` again

### Issue: Login fails
**Solution:** Run `python create_test_users.py` to recreate users

### Issue: GPS not working
**Solution:** Allow browser location access when prompted

### Issue: Exam timer not working
**Solution:** Ensure JavaScript is enabled in browser

### Issue: 404 errors on links
**Solution:** Check that all URLs are defined in `core/urls.py`

## Next Steps

After testing, you can:
1. Add more topics to modules
2. Create more assignments
3. Add more exam questions
4. Test assignment submission
5. Test exam taking
6. Test attendance marking with GPS

## Database Reset (if needed)

To start fresh:
```bash
# Delete database
del db.sqlite3

# Run migrations
python manage.py migrate

# Create users
python manage.py createsuperuser
python create_test_users.py

# Populate data
python populate_student_data.py
```

## Support

If you encounter any issues:
1. Check browser console for JavaScript errors
2. Check terminal for Django errors
3. Verify all migrations are applied
4. Ensure all URLs are correctly defined
5. Check that student has course assigned

## Status: READY FOR TESTING ✅

All features are implemented and working. The system is ready for comprehensive testing.
