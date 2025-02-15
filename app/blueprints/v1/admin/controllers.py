from flask_jwt_extended import jwt_required
from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions
from .services import igenerate_project_submission, igrade_student_project
from .services import iretrieve_projects_with_submissions, iretrieve_assigned_project_submissions


@jwt_required()
@admin_required
@handle_endpoint_exceptions
def grade_student_project():
    igrade_student_project()
    return format_json_responses(message="Grading successful")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def generate_project_submission(project_id):
    igenerate_project_submission(project_id)
    return format_json_responses(message="Project Submission Generated For Admin Successfully!")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_assigned_project_submissions(project_id):
    assigned_projects = iretrieve_assigned_project_submissions(project_id)
    return format_json_responses(data=assigned_projects)

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_projects_with_submissions():
    projects = iretrieve_projects_with_submissions()
    return format_json_responses(data={"projects": projects})
