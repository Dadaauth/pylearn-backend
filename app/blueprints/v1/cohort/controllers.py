from flask import request
from flask_jwt_extended import jwt_required

from .service import icreate_cohort, iget_cohort, iget_cohort_students, iupdate_cohort, idelete_cohort
from .service import iassign_mentor_to_cohorts, iremove_mentor_from_cohorts, iget_all_cohorts
from .service import iadd_students_to_cohort
from app.utils.helpers import admin_required, handle_endpoint_exceptions, format_json_responses


@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_cohort():
    icreate_cohort()
    return format_json_responses(201, message="Cohort created successfully")

@jwt_required()
@handle_endpoint_exceptions
def get_cohort(cohort_id):
    cohort = iget_cohort(cohort_id)
    return format_json_responses(data={"cohort": cohort})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def ud_cohort(cohort_id):
    """Update || Delete a Course"""
    if request.method == 'PATCH':
        iupdate_cohort(cohort_id)
    elif request.method == 'DELETE':
        idelete_cohort(cohort_id)
    return format_json_responses(message="Operation successful")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def add_students_to_cohort(cohort_id):
    iadd_students_to_cohort(cohort_id)
    return format_json_responses(message="Record update successful!")

@jwt_required()
@handle_endpoint_exceptions
def get_cohort_students(cohort_id):
    cohort_with_students = iget_cohort_students(cohort_id)
    return format_json_responses(data={"cohort": cohort_with_students})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def assign_mentor_to_cohorts():
    """Assigns a mentor to a list of cohorts"""
    iassign_mentor_to_cohorts()
    return format_json_responses(201, message="Mentor assigned to cohorts successfully")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def remove_mentor_from_cohorts():
    """Removes a mentor from a list of cohorts"""
    iremove_mentor_from_cohorts()
    return format_json_responses(message="Mentor removed from cohorts successfully")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def get_all_cohorts():
    cohorts = iget_all_cohorts()
    return format_json_responses(data={"cohorts": cohorts})