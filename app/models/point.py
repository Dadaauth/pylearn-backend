from logging import NullHandler
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column


from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class Point(BaseModel, Base):
    __tablename__ = "points"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    source = mapped_column(Enum("project", "practice", "streak"), nullable=False)
    source_id = mapped_column(String(60))
    value = mapped_column(Integer, nullable=False)

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "value", "source"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")