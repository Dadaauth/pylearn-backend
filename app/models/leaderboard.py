from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship


from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class LeaderBoard(BaseModel, Base):
    __tablename__ = "leaderboards"

    level = mapped_column(Enum("wood", "silver", "gold", "diamond"), nullable=False)
    students = relationship("LeaderBoardStudent")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "project_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
class LeaderBoardStudent(BaseModel, Base):
    __tablename__ = "leaderboard_students"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False, unique=True)
    leaderboard_id = mapped_column(ForeignKey("leaderboards.id"), nullable=False)

    leaderboard = relationship("LeaderBoard", back_populates="students")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "leaderboard_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")