from flask_jwt_extended import jwt_required, get_jwt_identity

from app.blueprints.project.services import create_new_project, fetch_projects, fetch_project_details_single
from app.blueprints.project.services import update_single_project_details, mark_a_project_as_done, _retrieve_projects_status
from .services import icreate_module, ifetch_modules
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_module():
    icreate_module()
    return format_json_responses(201, message="Resource created successfully!")

@jwt_required()
@handle_endpoint_exceptions
def fetch_modules():
    modules = ifetch_modules()
    return format_json_responses(data={"modules": modules})

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











@handle_endpoint_exceptions
def retrieve_projects_status():
    data = _retrieve_projects_status()
    return format_json_responses(data=data, message="Record retrieved successfully")

@handle_endpoint_exceptions
def mark_project_as_done():
    mark_a_project_as_done()
    return format_json_responses(message="Operation successfull")

@handle_endpoint_exceptions
def fetch_single():
    data = fetch_project_details_single()
    return format_json_responses(data=data, message="Resource retrieved successfully")

@handle_endpoint_exceptions
def update_single(id):
    update_single_project_details(id)
    return format_json_responses(message="Operation successful")