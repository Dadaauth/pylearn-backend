from datetime import datetime, timezone

from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import extract_request_data, retrieve_model_info
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student, Admin
from app.models.project import StudentProject, Project
from app.models.module import Module