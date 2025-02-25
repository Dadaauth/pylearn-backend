from flask import Blueprint
from app.blueprints.v1.project.controllers import create_project, fetch_projects_for_admin, fetch_single, update_single
from app.blueprints.v1.project.controllers import generate_project_submission, retrieve_assigned_project_submissions
from app.blueprints.v1.project.controllers import retrieve_projects_with_submissions, grade_student_project

project_bp = Blueprint('project', __name__)



# Admin and Mentor access only functionalities
project_bp.add_url_rule('/<course_id>/for-admin/all', view_func=fetch_projects_for_admin, methods=['GET'])
project_bp.add_url_rule('/<project_id>', view_func=fetch_single, methods=['GET'])
project_bp.add_url_rule("/<project_id>/submissions/generate", view_func=generate_project_submission, methods=["GET"])
project_bp.add_url_rule("/<project_id>/assigned_submissions", view_func=retrieve_assigned_project_submissions, methods=["GET"])
project_bp.add_url_rule("/<cohort_id>/projects/with_submissions", view_func=retrieve_projects_with_submissions, methods=["GET"])
project_bp.add_url_rule("/grade", view_func=grade_student_project, methods=["PATCH"])
project_bp.add_url_rule('/edit/<project_id>', view_func=update_single, methods=['PATCH'])
project_bp.add_url_rule('/create', view_func=create_project, methods=['POST'])
