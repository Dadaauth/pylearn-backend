from flask import Blueprint

from app.blueprints.v1.admin.controllers import retrieve_assigned_project_submissions, retrieve_projects_with_submissions
from app.blueprints.v1.admin.controllers import grade_student_project

admin_bp = Blueprint('admin', __name__)

admin_bp.add_url_rule("/<project_id>/assigned_submissions", view_func=retrieve_assigned_project_submissions, methods=["GET"])
admin_bp.add_url_rule("/projects/with_submissions", view_func=retrieve_projects_with_submissions, methods=["GET"])
admin_bp.add_url_rule("/project/grade", view_func=grade_student_project, methods=["PATCH"])