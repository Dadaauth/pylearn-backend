from flask_jwt_extended import get_jwt_identity

from app.models.user import Mentor, MentorCohort
from app.models.course import Course
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

def imentor_assigned_cohorts():
    mentor = Mentor.search(id=get_jwt_identity()["id"])
    if not mentor:
        raise NotFound(f"Mentor account not found!")
    if not mentor.cohorts:
        raise NotFound(f"No assigned cohorts to mentor")
    
    tmp = mentor.cohorts
    cohorts_list = []
    if isinstance(tmp, MentorCohort):
        course = Course.search(id=tmp.course_id)
        tmp = tmp.to_dict()
        tmp["course"] = course.to_dict()
        cohorts_list.append(tmp)
    if isinstance(tmp, list):
        for cohort in tmp:
            course = Course.search(id=cohort.course_id)
            cohort = cohort.to_dict()
            cohort["course"] = course.to_dict()
            cohorts_list.append(cohort)
    return cohorts_list

def imentor_assigned_cohorts_for_admin(mentor_id):
    mentor = Mentor.search(id=mentor_id)
    if not mentor:
        raise NotFound(f"Mentor with ID [{mentor_id}] not found!")
    if not mentor.cohorts:
        raise NotFound(f"No assigned cohorts to mentor with ID [{mentor_id}]")
    
    tmp = mentor.cohorts
    cohorts_list = []
    if isinstance(tmp, MentorCohort):
        course = Course.search(id=tmp.course_id)
        tmp = tmp.to_dict()
        tmp["course"] = course.to_dict()
        cohorts_list.append(tmp)
    if isinstance(tmp, list):
        for cohort in tmp:
            course = Course.search(id=cohort.course_id)
            cohort = cohort.to_dict()
            cohort["course"] = course.to_dict()
            cohorts_list.append(cohort)
    return cohorts_list