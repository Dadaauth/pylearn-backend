from flask_jwt_extended import jwt_required
from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions, retrieve_model_info
from .services import admin_create_new_student, all_students_data
from app.models.user import Student

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_new_student():
    admin_create_new_student()
    return format_json_responses(201, message="Student created successfully.")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def all_students():
    students_data = all_students_data()
    return format_json_responses(200, data={"students": students_data})