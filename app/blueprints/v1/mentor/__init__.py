from flask import Blueprint

from .controllers import all_mentors, activate_account

mentor_bp = Blueprint('mentor', __name__)


mentor_bp.add_url_rule('/account/activate', view_func=activate_account, methods=['POST'])

# Admin access only
mentor_bp.add_url_rule("/all", view_func=all_mentors, methods=["GET"])
