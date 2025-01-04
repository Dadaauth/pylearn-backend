from flask_jwt_extended import jwt_required
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions
from .services import activate_student_account, ifetch_modules_for_student, release_first_project

@handle_endpoint_exceptions
def activate_account():
    student_id = activate_student_account()
    release_first_project(student_id)
    return format_json_responses(200, message="Account activated successfully.")

@jwt_required()
@handle_endpoint_exceptions
def fetch_modules_for_student():
    modules = ifetch_modules_for_student()
    return format_json_responses(data={"modules": modules}, message="Record Retrieved Successfully!")