from flask import Blueprint
from app.blueprints.module.controllers import update_module, fetch_modules, create_module

module_bp = Blueprint('module', __name__)

module_bp.add_url_rule('/create', view_func=create_module, methods=['POST'])
module_bp.add_url_rule('/<module_id>/update', view_func=update_module, methods=['PATCH'])
module_bp.add_url_rule('/', view_func=fetch_modules, methods=['GET'], strict_slashes=False)
