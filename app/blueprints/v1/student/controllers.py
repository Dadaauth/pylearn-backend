from flask_jwt_extended import jwt_required
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required, mentor_required
from .services import activate_student_account, count_completed_modules, count_completed_projects
# from .services import ifetch_project_for_student, ifetch_current_projects, isubmit_student_project, irelease_next_project, ifetch_modules_for_student, release_first_project
from .services import all_students_data, iretrieve_students_with_no_cohort, student_create_new_account


@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def all_students():
    students_data = all_students_data()
    return format_json_responses(200, data={"students": students_data})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_students_with_no_cohort(course_id):
    students = iretrieve_students_with_no_cohort(course_id)
    return format_json_responses(data={"students": students})

@handle_endpoint_exceptions
def new_student_registration():
    student_create_new_account()
    return format_json_responses(201, message="Account created successfully.")

@jwt_required()
@handle_endpoint_exceptions
def countCompleted():
    modules = count_completed_modules()
    projects = count_completed_projects()
    return format_json_responses(data={"modules": modules, "projects": projects})

# @jwt_required()
# @handle_endpoint_exceptions
# def submitProject(project_id):
#     isubmit_student_project(project_id)
#     irelease_next_project(project_id)
#     return format_json_responses(message="Project Submitted Successfully!")

# @jwt_required()
# @handle_endpoint_exceptions
# def fetchcurrentprojects():
#     projects = ifetch_current_projects()
#     return format_json_responses(data={"projects": projects}, message="Projects Retrieved successfully")

# @jwt_required()
# @handle_endpoint_exceptions
# def fetchproject(project_id):
#     project = ifetch_project_for_student(project_id)
#     return format_json_responses(data={"project": project})

# @handle_endpoint_exceptions
# def activate_account():
#     student_id = activate_student_account()
#     release_first_project(student_id)
#     return format_json_responses(200, message="Account activated successfully.")

# @jwt_required()
# @handle_endpoint_exceptions
# def fetch_modules_for_student():
#     modules = ifetch_modules_for_student()
#     return format_json_responses(data={"modules": modules}, message="Record Retrieved Successfully!")