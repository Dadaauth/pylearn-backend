from flask import Blueprint
from app.blueprints.auth.controllers import login, register, logout, refresh

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/register', view_func=register, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])
auth_bp.add_url_rule('/refresh', view_func=refresh, methods=['GET'])
