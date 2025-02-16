from flask import Blueprint

from .controllers import all_mentors

mentor_bp = Blueprint('mentor', __name__)


# Admin access only
mentor_bp.add_url_rule("/all", view_func=all_mentors, methods=["GET"])
