from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, ENUM
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys

class Project(BaseModel, Base):
    __tablename__ = "projects"

    title = mapped_column(String(300), nullable=False)
    description = mapped_column(String(300), nullable=False)
    content = mapped_column(LONGTEXT, nullable=False)

    def __init__(self, **kwargs):
        """
            Initialize a new User instance.
            Args:
                **kwargs: Arbitrary keyword arguments containing user attributes.
            Raises:
                ValueError: If any of the required keys ('first_name', 'last_name', 'email', 'password') are missing.
            Attributes:
                password (str): The hashed password of the user.
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'title', 'content'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")


class StudentProject(BaseModel, Base):
    __tablename__ = "student_projects"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    project_id = mapped_column(ForeignKey("projects.id"), nullable=False)
    status = mapped_column(ENUM("pending", "completed"), default="pending")

    def __init__(self, **kwargs):
        """
            Initialize a new User instance.
            Args:
                **kwargs: Arbitrary keyword arguments containing user attributes.
            Raises:
                ValueError: If any of the required keys ('first_name', 'last_name', 'email', 'password') are missing.
            Attributes:
                password (str): The hashed password of the user.
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "project_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")