from flask import Blueprint

from .controllers import create_cohort, get_cohort, get_cohort_students, ud_cohort

cohort_bp = Blueprint('cohort', __name__)

cohort_bp.add_url_rule('/create', view_func=create_cohort, methods=['POST'])
cohort_bp.add_url_rule('/<cohort_id>', view_func=get_cohort, methods=['GET'])
cohort_bp.add_url_rule('/<cohort_id>', view_func=ud_cohort, methods=['PATCH', 'DELETE'])
cohort_bp.add_url_rule('/<cohort_id>/students', view_func=get_cohort_students, methods=['GET'])