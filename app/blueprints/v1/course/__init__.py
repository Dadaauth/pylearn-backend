from flask import Blueprint
from .controllers import create_course, retrieve_all_courses, retrieve_single_course, retrieve_single_course_with_modules
from .controllers import retrieve_all_course_data, ud_course

course_bp = Blueprint('course', __name__)

course_bp.add_url_rule('/create', view_func=create_course, methods=['POST'])
course_bp.add_url_rule('/all', view_func=retrieve_all_courses, methods=['GET'])
course_bp.add_url_rule('/<course_id>', view_func=retrieve_single_course, methods=['GET'])
course_bp.add_url_rule('/<course_id>', view_func=ud_course, methods=['PATCH', 'DELETE'])
course_bp.add_url_rule('/<course_id>/modules', view_func=retrieve_single_course_with_modules, methods=['GET'])
course_bp.add_url_rule('/<course_id>/all', view_func=retrieve_all_course_data, methods=["GET"])