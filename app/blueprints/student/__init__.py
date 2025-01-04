from flask import Blueprint
from app.blueprints.student.controllers import activate_account, fetch_modules_for_student

student_bp = Blueprint('student', __name__)

student_bp.add_url_rule('/account/activate', view_func=activate_account, methods=['POST'])
student_bp.add_url_rule('/modules', view_func=fetch_modules_for_student, methods=['GET'])