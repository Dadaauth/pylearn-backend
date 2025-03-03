import os
from datetime import timedelta

from flask import Flask, g
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app(environment="development"):
    app = Flask(__name__)
    CORS(app)

    if environment == "production":
        load_dotenv(".env.production")
    else:
        load_dotenv()

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=7)
    )
    jwt = JWTManager(app)

    from app.blueprints import register_blueprints
    from app.models.user import Admin, Mentor, Student
    from app.models import storage
    
    @jwt.user_lookup_loader
    def user_loader_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        if identity['role'] == 'admin':
            return Admin.search(id=identity['id'])
        elif identity['role'] == 'mentor':
            return Mentor.search(id=identity['id'])
        elif identity['role'] == 'student':
            return Student.search(id=identity['id'])
        return None
    
    @app.before_request
    def create_session():
        # Load a new Storage object
        g.db_storage = storage
        g.db_session = storage.load_session()

    @app.teardown_request
    def remove_session(exception=None):
        if hasattr(g, 'db_storage'):
            # Close the session and remove
            # Session from scoped_session
            # remember to lose other resources like engine
            g.db_session.close()

    register_blueprints(app)
    return app