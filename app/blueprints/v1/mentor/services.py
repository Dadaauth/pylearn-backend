
from app.models.user import Mentor
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, NotFound, InternalServerError

def all_mentors_data():
    mentors = Mentor.all()
    mentors_data = [retrieve_model_info(mentor, ["id", \
        "first_name", "last_name",\
        "email", "status",\
        "username"])\
        for mentor in mentors]
    mentors_data = list(reversed(mentors_data))
    return mentors_data

def activate_mentor_account():
    data = extract_request_data("json")
    email = data.get("email")
    if not email:
        raise BadRequest("Missing required field: email")

    mentor = Mentor.search(email=email)
    if not mentor:
        raise NotFound(f"Mentor with Email {email} not found")
    
    if isinstance(mentor, list):
        raise InternalServerError("Multiple mentors with same email address")
    
    if not (data.get("username") and data.get("password") and data.get("phone")):
        raise BadRequest("Missing required field(s): username, password, phone")

    if mentor.status == "active":
        raise BadRequest("Account Activated Already!!")

    mentor.update(**{
        "username": data["username"],
        "password": data["password"],
        "phone": data["phone"],
        "status": "active"
    })
    mentor.save()
