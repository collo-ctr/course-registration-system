from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Student, Course, Registration

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register/<int:course_id>')
def register_course(course_id):
    """Register student for a course"""
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))
    
    student = Student.query.get(session['user_id'])
    course = Course.query.get(course_id)
    
    if not course:
        flash('Course not found!', 'error')
        return redirect(url_for('dashboard'))
    
    if course.is_full():
        flash('Course is full! Maximum capacity reached.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if already registered
    existing = Registration.query.filter_by(
        student_id=student.id,
        course_id=course_id
    ).first()
    
    if existing:
        flash(f'You are already registered for {course.name}', 'warning')
    else:
        registration = Registration(student_id=student.id, course_id=course_id)
        course.enrolled += 1
        db.session.add(registration)
        db.session.commit()
        flash(f'✅ Successfully registered for {course.name}!', 'success')
    
    return redirect(url_for('dashboard'))

@registration_bp.route('/drop/<int:course_id>')
def drop_course(course_id):
    """Drop a registered course"""
    if 'user_id' not in session:
        flash('⚠️ Please login first', 'warning')
        return redirect(url_for('auth.login'))
    
    student = Student.query.get(session['user_id'])
    course = Course.query.get(course_id)
    
    registration = Registration.query.filter_by(
        student_id=student.id,
        course_id=course_id
    ).first()
    
    if registration:
        course.enrolled -= 1
        db.session.delete(registration)
        db.session.commit()
        flash(f'Dropped {course.name} successfully!', 'success')
    else:
        flash('Course not found in your registration!', 'error')
    
    return redirect(url_for('dashboard'))

@registration_bp.route('/registered')
def view_registered():
    """View all registered courses"""
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))
    
    student = Student.query.get(session['user_id'])
    registered_courses = [reg.course for reg in student.registrations]
    total_credits = sum(course.credits for course in registered_courses)
    
    return render_template('registered.html', 
                         courses=registered_courses,
                         user=student,
                         total_credits=total_credits)
