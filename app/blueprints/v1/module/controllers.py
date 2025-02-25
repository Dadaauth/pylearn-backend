from flask_jwt_extended import jwt_required

from .services import icreate_module, ifetch_modules, iupdate_module
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_module():
    icreate_module()
    return format_json_responses(201, message="Resource created successfully!")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def update_module(module_id):
    iupdate_module(module_id)
    return format_json_responses(message="Record updated successfully!")

@jwt_required()
@handle_endpoint_exceptions
def fetch_modules(course_id):
    modules = ifetch_modules(course_id)
    return format_json_responses(data={"modules": modules})
