from datetime import datetime
from uuid import uuid4
from app.utils.helpers import extract_request_data, retrieve_model_info
from app.utils.error_extensions import BadRequest
from app.models.user import Student

def all_students_data():
    students = Student.all()
    students_data = [retrieve_model_info(student, ["id", \
                                                   "first_name", "last_name",\
                                                    "email", "registration_number", "status",\
                                                    "username"])\
                    for student in students]
    students_data = list(reversed(students_data))
    return students_data

def admin_create_new_student():
    data = extract_request_data("json")
    if not (data.get("first_name") and data.get("last_name") and data.get("email")):
        raise BadRequest("Missing required field(s): first_name, last_name, email")
    
    student_count = Student.count() + 1
    registration_number = f"{datetime.now().year}/C1/{str(student_count).zfill(4)}"
    student_details = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "username": str(uuid4()),
        "password": "placeholder",
        "status": "inactive",
        "registration_number": registration_number
    }
    Student(**student_details).save()