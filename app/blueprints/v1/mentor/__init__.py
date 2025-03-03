from flask import Blueprint

from .controllers import all_mentors, activate_account, mentor_assigned_cohorts, mentor_assigned_cohorts_for_admin
from .controllers import single_project_page

mentor_bp = Blueprint('mentor', __name__)


mentor_bp.add_url_rule('/account/activate', view_func=activate_account, methods=['POST'])
mentor_bp.add_url_rule("/assigned_cohorts", view_func=mentor_assigned_cohorts, methods=["GET"])
mentor_bp.add_url_rule('/project/<project_id>', view_func=single_project_page, methods=["GET"])

# Admin access only
mentor_bp.add_url_rule("/all", view_func=all_mentors, methods=["GET"])
mentor_bp.add_url_rule("/<mentor_id>/assigned_cohorts", view_func=mentor_assigned_cohorts_for_admin, methods=["GET"])