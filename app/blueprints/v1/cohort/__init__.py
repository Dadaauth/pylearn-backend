from flask import Blueprint

from .controllers import create_cohort, get_cohort, get_cohort_students, ud_cohort
from .controllers import assign_mentor_to_cohorts, remove_mentor_from_cohorts, get_all_cohorts
from .controllers import add_students_to_cohort

cohort_bp = Blueprint('cohort', __name__)

cohort_bp.add_url_rule('/create', view_func=create_cohort, methods=['POST'])
cohort_bp.add_url_rule('/all', view_func=get_all_cohorts, methods=['GET'])
cohort_bp.add_url_rule('/<cohort_id>', view_func=get_cohort, methods=['GET'])
cohort_bp.add_url_rule('/<cohort_id>', view_func=ud_cohort, methods=['PATCH', 'DELETE'])
cohort_bp.add_url_rule('/<cohort_id>/students', view_func=get_cohort_students, methods=['GET'])
cohort_bp.add_url_rule('/<cohort_id>/add-students', view_func=add_students_to_cohort, methods=['POST'])