from app.blueprints.auth import auth_bp
from app.blueprints.project import project_bp
from app.blueprints.admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(project_bp, url_prefix='/api/v1/project')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')