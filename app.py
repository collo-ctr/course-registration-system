from flask import Flask, render_template, session, flash, redirect, url_for
from models import db, bcrypt, Student, Course, Registration
from auth import auth_bp
from dashboard import dashboard_bp
from registration import registration_bp
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(registration_bp)

# ----- CREATE TABLES AND SEED DATA -----
with app.app_context():
    db.create_all()
    
    # Seed courses if database is empty
    if Course.query.count() == 0:
        courses = [
            Course(
                code='SE401', 
                name='Software Engineering', 
                credits=3,
                instructor='Dr. Kamau', 
                description='Software development lifecycle, Agile methodologies, Scrum, and project management.'
            ),
            Course(
                code='DB402', 
                name='Database Systems', 
                credits=3,
                instructor='Prof. Otieno', 
                description='SQL, NoSQL, database design, normalization, and query optimization.'
            ),
            Course(
                code='WEB403', 
                name='Web Development', 
                credits=3,
                instructor='Mr. Kiprop', 
                description='HTML, CSS, JavaScript, Flask, REST APIs, and modern web frameworks.'
            ),
            Course(
                code='NS404', 
                name='Network Security', 
                credits=3,
                instructor='Dr. Akinyi', 
                description='Network protocols, security threats, encryption, and firewalls.'
            ),
            Course(
                code='MAD405', 
                name='Mobile App Development', 
                credits=3,
                instructor='Ms. Chebet', 
                description='Android and iOS development with Flutter and React Native.'
            ),
            Course(
                code='AI406', 
                name='Artificial Intelligence', 
                credits=4,
                instructor='Prof. Mwangi', 
                description='Machine learning, neural networks, deep learning, and AI applications.'
            ),
        ]
        db.session.add_all(courses)
        db.session.commit()
        print("Sample courses seeded successfully!")

# ----- HOME ROUTE (Redirects to Login) -----
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# ----- ERROR HANDLERS -----
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ----- CONTEXT PROCESSOR (Inject user into templates) -----
@app.context_processor
def inject_user():
    if 'user_id' in session:
        student = Student.query.get(session['user_id'])
        return dict(current_user=student)
    return dict(current_user=None)

# ----- RUN THE APP -----
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
