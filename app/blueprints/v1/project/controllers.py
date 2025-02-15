from flask_jwt_extended import jwt_required

from app.blueprints.v1.project.services import create_new_project, fetch_projects, ifetch_project, igenerate_project_submission
from app.blueprints.v1.project.services import update_single_project_details, mark_a_project_as_done, _retrieve_projects_status
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required, mentor_required

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def generate_project_submission(project_id):
    """For Mentors Only!!!"""
    igenerate_project_submission(project_id)
    return format_json_responses(message="Project Submission Generated For Mentor Successfully!")

@jwt_required()
@handle_endpoint_exceptions
def fetch_projects_for_module():
    projects = fetch_projects()
    return format_json_responses(data={"projects": projects})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_project():
    create_new_project()
    return format_json_responses(201, message="Resource created successfully")

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def fetch_single(project_id):
    project = ifetch_project(project_id)
    return format_json_responses(data={"project": project})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def update_single(project_id):
    update_single_project_details(project_id)
    return format_json_responses(message="Resource Updated Successfully!")













@handle_endpoint_exceptions
def retrieve_projects_status():
    data = _retrieve_projects_status()
    return format_json_responses(data=data, message="Record retrieved successfully")

@handle_endpoint_exceptions
def mark_project_as_done():
    mark_a_project_as_done()
    return format_json_responses(message="Operation successfull")
