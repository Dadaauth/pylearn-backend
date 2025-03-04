from flask_jwt_extended import jwt_required

from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required, extract_request_data
from .services import count_completed_modules, count_completed_projects, submit_project
from .services import iretrieve_students_with_no_cohort, student_create_new_account
from .services import ifetch_current_projects, get_project_data, get_extra_project_details
from .services import get_course_and_cohort_id, get_modules, append_projects_to_modules
from .services import send_welcome_email_for_student


@jwt_required()
@handle_endpoint_exceptions
def allprojects_page():
    course_id, cohort_id = get_course_and_cohort_id()
    modules = get_modules(course_id)
    modules = append_projects_to_modules(modules, cohort_id)
    return format_json_responses(data={"modules": modules})

@jwt_required()
@handle_endpoint_exceptions
def submitProject(project_id):
    data = extract_request_data("json")
    submit_project(project_id, data)
    return format_json_responses(message="Project submission successful")

@jwt_required()
@handle_endpoint_exceptions
def single_project_page(project_id):
    """ Retrieve data for the single
        project view page for a student.
    """
    project = get_project_data(project_id)
    project = get_extra_project_details(project)
    next_project = get_project_data(project["next_project_id"])
    prev_project = get_project_data(project["prev_project_id"])
    return format_json_responses(data={"project": project, "next_project": next_project, "prev_project": prev_project})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_students_with_no_cohort(course_id):
    students = iretrieve_students_with_no_cohort(course_id)
    return format_json_responses(data={"students": students})

@handle_endpoint_exceptions
def new_student_registration():
    student_details = student_create_new_account()
    send_welcome_email_for_student(student_details)
    return format_json_responses(201, message="Account created successfully.")

@jwt_required()
@handle_endpoint_exceptions
def countCompleted():
    modules = count_completed_modules()
    projects = count_completed_projects()
    return format_json_responses(data={"modules": modules, "projects": projects})

@jwt_required()
@handle_endpoint_exceptions
def fetchcurrentprojects():
    projects = ifetch_current_projects()
    return format_json_responses(data={"projects": projects}, message="Projects Retrieved successfully")
