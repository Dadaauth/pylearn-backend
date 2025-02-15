from flask import Blueprint
from app.blueprints.v1.admin.controllers import all_students, generate_project_submission
from app.blueprints.v1.admin.controllers import retrieve_assigned_project_submissions, retrieve_projects_with_submissions
from app.blueprints.v1.admin.controllers import grade_student_project, fetchproject

admin_bp = Blueprint('admin', __name__)

admin_bp.add_url_rule("/students", view_func=all_students, methods=["GET"])
admin_bp.add_url_rule('/project/<project_id>', strict_slashes=False, view_func=fetchproject, methods=['GET'])
admin_bp.add_url_rule("/<project_id>/submissions/generate", view_func=generate_project_submission, methods=["GET"])
admin_bp.add_url_rule("/<project_id>/assigned_submissions", view_func=retrieve_assigned_project_submissions, methods=["GET"])
admin_bp.add_url_rule("/projects/with_submissions", view_func=retrieve_projects_with_submissions, methods=["GET"])
admin_bp.add_url_rule("/project/grade", view_func=grade_student_project, methods=["PATCH"])