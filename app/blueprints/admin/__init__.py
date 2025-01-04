from flask import Blueprint
from app.blueprints.admin.controllers import create_new_student, all_students

admin_bp = Blueprint('admin', __name__)

admin_bp.add_url_rule("/student/create", view_func=create_new_student, methods=["POST"])
admin_bp.add_url_rule("/students", view_func=all_students, methods=["GET"])
