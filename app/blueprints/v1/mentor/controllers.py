from flask_jwt_extended import jwt_required

from app.utils.helpers import admin_required, mentor_required, format_json_responses, handle_endpoint_exceptions, format_json_responses
from .services import all_mentors_data, activate_mentor_account, imentor_assigned_cohorts, imentor_assigned_cohorts_for_admin
from .services import get_project_data, get_extra_project_details


@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def single_project_page(project_id):
    project = get_project_data(project_id)
    project = get_extra_project_details(project)
    next_project = get_project_data(project["next_project_id"])
    prev_project = get_project_data(project["prev_project_id"])
    return format_json_responses(data={"project": project, "next_project": next_project, "prev_project": prev_project})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def all_mentors():
    mentors = all_mentors_data()
    return format_json_responses(200, data={"mentors": mentors})

@handle_endpoint_exceptions
def activate_account():
    activate_mentor_account()
    return format_json_responses(200, message="Account activated successfully.")

@jwt_required()
@mentor_required
@handle_endpoint_exceptions
def mentor_assigned_cohorts():
    cohorts = imentor_assigned_cohorts()
    return format_json_responses(data={"cohorts": cohorts})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def mentor_assigned_cohorts_for_admin(mentor_id):
    cohorts = imentor_assigned_cohorts_for_admin(mentor_id)
    return format_json_responses(data={"cohorts": cohorts})