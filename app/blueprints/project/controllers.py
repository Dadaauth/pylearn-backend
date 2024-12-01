from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import create_access_token

from app.blueprints.project.services import create_new_project, fetch_project_details, fetch_project_details_single
from app.blueprints.project.services import update_single_project_details
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required

# @jwt_required()
# @admin_required
@handle_endpoint_exceptions
def create():
    create_new_project()
    return format_json_responses(201, message="Resource created successfully")

@handle_endpoint_exceptions
def fetch():
    data = fetch_project_details()
    return format_json_responses(data=data, message="Resource retrieved successfully")

@handle_endpoint_exceptions
def fetch_single():
    data = fetch_project_details_single()
    return format_json_responses(data=data, message="Resource retrieved successfully")

@handle_endpoint_exceptions
def update_single(id):
    update_single_project_details(id)
    return format_json_responses(message="Operation successful")