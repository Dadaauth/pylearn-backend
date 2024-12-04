from flask import Blueprint
from app.blueprints.project.controllers import create, fetch, fetch_single, update_single
from app.blueprints.project.controllers import mark_project_as_done

project_bp = Blueprint('project', __name__)

project_bp.add_url_rule('/create', view_func=create, methods=['POST'])
project_bp.add_url_rule('/fetch/all', view_func=fetch, methods=['GET'])
project_bp.add_url_rule('/fetch/single', view_func=fetch_single, methods=['GET'])
project_bp.add_url_rule('/edit/<id>', view_func=update_single, methods=['PATCH'])
project_bp.add_url_rule('/mark/done', view_func=mark_project_as_done, methods=['PATCH'])
