from flask import Blueprint

from .controllers import retrieve_students_with_no_cohort, countCompleted, new_student_registration
from .controllers import fetchcurrentprojects, single_project_page, submitProject, allprojects_page

student_bp = Blueprint('student', __name__)

# Admin and Mentor access only functionalities
student_bp.add_url_rule("/no-cohort/<course_id>", view_func=retrieve_students_with_no_cohort, methods=["GET"])

# Student Functionalities
student_bp.add_url_rule('/project/<project_id>', view_func=single_project_page, methods=['GET'])
student_bp.add_url_rule('/projects', view_func=allprojects_page, methods=['GET'])
student_bp.add_url_rule('/project/<project_id>/submit', view_func=submitProject, methods=['POST'])
student_bp.add_url_rule("/register", view_func=new_student_registration, methods=["POST"])
student_bp.add_url_rule('/projects/current', view_func=fetchcurrentprojects, methods=['GET'])
student_bp.add_url_rule('/count/completed', strict_slashes=False, view_func=countCompleted, methods=["GET"])
