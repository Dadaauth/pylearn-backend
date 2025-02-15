from flask import Blueprint
from app.blueprints.v1.project.controllers import create_project, fetch_projects_for_module, fetch_single, update_single
from app.blueprints.v1.project.controllers import mark_project_as_done, retrieve_projects_status

project_bp = Blueprint('project', __name__)

project_bp.add_url_rule('/all', view_func=fetch_projects_for_module, methods=['GET'])
project_bp.add_url_rule('/create', view_func=create_project, methods=['POST'])
project_bp.add_url_rule('/<project_id>', view_func=fetch_single, methods=['GET'])
project_bp.add_url_rule('/edit/<project_id>', view_func=update_single, methods=['PATCH'])



# project_bp.add_url_rule('/mark/done', view_func=mark_project_as_done, methods=['PATCH'])
# project_bp.add_url_rule('/status', view_func=retrieve_projects_status, methods=['POST'])
