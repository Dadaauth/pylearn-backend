from app.blueprints.auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')