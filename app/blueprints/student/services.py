

from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student


def activate_student_account():
    data = extract_request_data("json")
    registration_number = data.get("registration_number")
    if not registration_number:
        raise BadRequest("Missing required field: registration_number")

    student = Student.search(registration_number=registration_number)
    if not student:
        raise NotFound(f"Student with Registration Number {registration_number} not found")
    
    if not (data.get("username") and data.get("password") and data.get("phone")):
        raise BadRequest("Missing required field(s): username, password, phone")

    student.update(**{
        "username": data["username"],
        "password": data["password"],
        "phone": data["phone"],
        "status": "active"
    })
    student.save()
    