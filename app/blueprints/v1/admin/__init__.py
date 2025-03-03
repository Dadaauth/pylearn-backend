from flask import Blueprint

from .controllers import adminprojects_page, single_project_page, project_create_page
from .controllers import project_edit_page, adminmentors_page

admin_bp = Blueprint('admin', __name__)


admin_bp.add_url_rule('/<course_id>/projects', view_func=adminprojects_page, methods=["GET"])
admin_bp.add_url_rule('/mentors', view_func=adminmentors_page, methods=["GET", "PATCH"])
admin_bp.add_url_rule('/<course_id>/project/new', view_func=project_create_page, methods=["GET", "POST"])
admin_bp.add_url_rule('/project/<project_id>/edit', view_func=project_edit_page, methods=["GET", "PATCH"])
admin_bp.add_url_rule('/project/<project_id>', view_func=single_project_page, methods=["GET"])
