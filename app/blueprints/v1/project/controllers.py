from flask_jwt_extended import jwt_required

from app.blueprints.v1.project.services import ifetch_project, igenerate_project_submission
from app.blueprints.v1.project.services import update_single_project_details, ifetch_projects_for_cohort
from app.blueprints.v1.project.services import iretrieve_assigned_project_submissions, igrade_student_project, iretrieve_projects_with_submissions
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, admin_required, mentor_required


@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def grade_student_project():
    igrade_student_project()
    return format_json_responses(message="Grading successful")

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def retrieve_projects_with_submissions(cohort_id):
    projects = iretrieve_projects_with_submissions(cohort_id)
    return format_json_responses(data={"projects": projects})

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def retrieve_assigned_project_submissions(project_id):
    """For Mentors Only!!!"""
    assigned_projects = iretrieve_assigned_project_submissions(project_id)
    return format_json_responses(data=assigned_projects)

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def generate_project_submission(project_id):
    """For Mentors Only!!!"""
    igenerate_project_submission(project_id)
    return format_json_responses(message="Project Submission Generated For Mentor Successfully!")

@jwt_required()
@handle_endpoint_exceptions
def fetch_projects_for_cohort(course_id):
    projects = ifetch_projects_for_cohort(course_id)
    return format_json_responses(data={"projects": projects})

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def fetch_single(project_id):
    project = ifetch_project(project_id)
    return format_json_responses(data={"project": project})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def update_single(project_id):
    update_single_project_details(project_id)
    return format_json_responses(message="Resource Updated Successfully!")
