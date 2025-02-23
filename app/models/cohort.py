from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import ENUM

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class Cohort(BaseModel, Base):
    __tablename__ = "cohorts"

    # Example Cohort-1
    name = mapped_column(String(60), nullable=False)
    status = mapped_column(ENUM("pending", "in-progress", "completed"), default="pending", nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)

    course = relationship("Course")
    students = relationship("Student", back_populates="cohort")
    mentors = relationship("MentorCohort", back_populates="cohort")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"name", "course_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")

