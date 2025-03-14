from flask_jwt_extended import get_jwt_identity

from app.models.user import Mentor, MentorCohort, Admin
from app.models.course import Course
from app.models.project import AdminProject
from app.models.module import Module
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, NotFound, InternalServerError

def get_extra_project_details(project):
    author = Admin.search(id=project["author_id"])
    if author:
        project["author"] = author.to_dict()
    return project

def get_project_data(project_id):
    if not project_id: return
    project = AdminProject.search(id=project_id)
    if not project: raise NotFound("Project not found")
    project_dict = project.to_dict()

    module = Module.search(id=project.module_id)
    if module:
        project_dict["module"] = module.to_dict()
    return project_dict

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
        cohort = tmp.cohort
        course = cohort.course.to_dict()
        cohort = cohort.to_dict()
        cohort["course"] = course
        cohorts_list.append(cohort)
    if isinstance(tmp, list):
        for mentor_cohort in tmp:
            cohort = mentor_cohort.cohort
            course = cohort.course.to_dict()
            cohort = cohort.to_dict()
            cohort["course"] = course
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
        cohort = tmp.cohort
        course = cohort.course.to_dict()
        cohort = cohort.to_dict()
        cohort["course"] = course
        cohorts_list.append(cohort)
    if isinstance(tmp, list):
        for mentor_cohort in tmp:
            cohort = mentor_cohort.cohort
            course = cohort.course.to_dict()
            cohort = cohort.to_dict()
            cohort["course"] = course
            cohorts_list.append(cohort)
    return cohorts_list