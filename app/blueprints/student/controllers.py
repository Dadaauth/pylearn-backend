from app.utils.helpers import format_json_responses, handle_endpoint_exceptions
from .services import activate_student_account

@handle_endpoint_exceptions
def activate_account():
    activate_student_account()
    return format_json_responses(200, message="Account activated successfully.")