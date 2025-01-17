from flask import Blueprint
from app.blueprints.student.controllers import activate_account, fetch_modules_for_student, fetchproject
from app.blueprints.student.controllers import fetchcurrentprojects, submitProject

student_bp = Blueprint('student', __name__)

student_bp.add_url_rule('/account/activate', view_func=activate_account, methods=['POST'])
student_bp.add_url_rule('/modules', view_func=fetch_modules_for_student, methods=['GET'])
student_bp.add_url_rule('/project/<project_id>', view_func=fetchproject, methods=['GET'])
student_bp.add_url_rule('/projects/current', view_func=fetchcurrentprojects, methods=['GET'])

student_bp.add_url_rule('/project/<project_id>/submit', view_func=submitProject, methods=['POST'])