from flask import request
from flask_jwt_extended import jwt_required

from .service import icreate_course, iretrieve_all_courses, iretrieve_single_course, iretrieve_single_course_with_modules
from .service import iretrieve_all_course_data, iupdate_course, idelete_course
from app.utils.helpers import admin_required, handle_endpoint_exceptions, format_json_responses

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_course():
    icreate_course()
    return format_json_responses(201, message="Course creation successful")

@jwt_required()
@handle_endpoint_exceptions
def retrieve_all_courses():
    courses = iretrieve_all_courses()
    return format_json_responses(data={"courses": courses})

@jwt_required()
@handle_endpoint_exceptions
def retrieve_single_course(course_id):
    course = iretrieve_single_course(course_id)
    return format_json_responses(data={"course": course})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def ud_course(course_id):
    """Update || Delete a Course"""
    if request.method == 'PATCH':
        iupdate_course(course_id)
    elif request.method == 'DELETE':
        idelete_course(course_id)
    return format_json_responses(message="Operation successful")

@jwt_required()
@handle_endpoint_exceptions
def retrieve_single_course_with_modules(course_id):
    course_with_modules = iretrieve_single_course_with_modules(course_id)
    return format_json_responses(data={"course": course_with_modules})

def retrieve_all_course_data(course_id):
    data = iretrieve_all_course_data(course_id)
    return format_json_responses(data={"course": data})