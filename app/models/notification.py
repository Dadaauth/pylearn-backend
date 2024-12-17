from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class Notification(BaseModel, Base):
    __tablename__ = "notifications"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    message = mapped_column(String(300), nullable=False)
    source = mapped_column(Enum("message", "point", "streak", "project", "module", "other"), nullable=False)
    source_id = mapped_column(String(60)) # Must not be a Foreign Key

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "message", "source"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")