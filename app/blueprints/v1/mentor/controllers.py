from flask_jwt_extended import jwt_required

from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions, format_json_responses
from .services import all_mentors_data

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def all_mentors():
    mentors = all_mentors_data()
    return format_json_responses(200, data={"mentors": mentors})
