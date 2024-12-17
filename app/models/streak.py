from sqlalchemy import ForeignKey, Integer, String, null
from sqlalchemy.orm import mapped_column

from app.models.basemodel import BaseModel
from app.models.base import Base
from app.utils.helpers import has_required_keys


class Streak(BaseModel, Base):
    __tablename__ = "streaks"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    frequency = mapped_column(Integer, nullable=False, default=0)
    count = mapped_column(Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")