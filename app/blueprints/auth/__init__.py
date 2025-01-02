from flask import Blueprint
from app.blueprints.auth.controllers import get_user_details, login, register, logout, refresh, check_user_role, is_logged_in

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/user/role', view_func=check_user_role, methods=['GET'])
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/register', view_func=register, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])
auth_bp.add_url_rule('/refresh', view_func=refresh, methods=['GET'])
auth_bp.add_url_rule('/is_logged_in', view_func=is_logged_in, methods=['GET'])
auth_bp.add_url_rule('/basic_user_details', view_func=get_user_details, methods=['GET'])