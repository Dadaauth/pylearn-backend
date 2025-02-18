from app.blueprints.v1.auth import auth_bp
from app.blueprints.v1.module import module_bp
from app.blueprints.v1.project import project_bp
from app.blueprints.v1.admin import admin_bp
from app.blueprints.v1.mentor import mentor_bp
from app.blueprints.v1.student import student_bp
from app.blueprints.v1.course import course_bp
from app.blueprints.v1.cohort import cohort_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(module_bp, url_prefix='/api/v1/module')
    app.register_blueprint(project_bp, url_prefix='/api/v1/project')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(mentor_bp, url_prefix='/api/v1/mentor')
    app.register_blueprint(student_bp, url_prefix='/api/v1/student')
    app.register_blueprint(course_bp, url_prefix='/api/v1/course')
    app.register_blueprint(cohort_bp, url_prefix='/api/v1/cohort')