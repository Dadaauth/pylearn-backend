from app.blueprints.auth import auth_bp
from app.blueprints.module import module_bp
from app.blueprints.project import project_bp
from app.blueprints.admin import admin_bp
from app.blueprints.student import student_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(module_bp, url_prefix='/api/v1/module')
    app.register_blueprint(project_bp, url_prefix='/api/v1/project')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(student_bp, url_prefix='/api/v1/student')