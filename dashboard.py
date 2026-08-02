from flask import Blueprint, render_template, session, flash, redirect, url_for
from models import db, Student, Course

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Main dashboard showing available and registered courses"""
    if 'user_id' not in session:
        flash('⚠️ Please login first', 'warning')
        return redirect(url_for('auth.login'))
    
    student = Student.query.get(session['user_id'])
    all_courses = Course.query.all()
    registered_courses = [reg.course for reg in student.registrations]
    
    return render_template('dashboard.html', 
                         courses=all_courses,
                         registered=registered_courses,
                         user=student)

@dashboard_bp.route('/course/<int:course_id>')
def course_details(course_id):
    """View course details page"""
    if 'user_id' not in session:
        flash('⚠️ Please login first', 'warning')
        return redirect(url_for('auth.login'))
    
    course = Course.query.get(course_id)
    if not course:
        flash('❌ Course not found!', 'error')
        return redirect(url_for('dashboard'))
    
    student = Student.query.get(session['user_id'])
    is_registered = any(reg.course_id == course_id for reg in student.registrations)
    
    return render_template('course_details.html', 
                         course=course,
                         is_registered=is_registered,
                         user=student)
