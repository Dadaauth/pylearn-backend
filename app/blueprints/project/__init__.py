from flask import Blueprint
from app.blueprints.project.controllers import create, fetch

project_bp = Blueprint('project', __name__)

project_bp.add_url_rule('/create', view_func=create, methods=['POST'])
project_bp.add_url_rule('/fetch', view_func=fetch, methods=['GET'])
