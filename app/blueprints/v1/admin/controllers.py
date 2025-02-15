from flask_jwt_extended import jwt_required
from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions, retrieve_model_info
from .services import all_students_data, ifetch_project, igenerate_project_submission, igrade_student_project
from .services import iretrieve_projects_with_submissions, iretrieve_assigned_project_submissions


@jwt_required()
@admin_required
@handle_endpoint_exceptions
def fetchproject(project_id):
    project = ifetch_project(project_id)
    return format_json_responses(data={"project": project})

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

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def all_students():
    students_data = all_students_data()
    return format_json_responses(200, data={"students": students_data})