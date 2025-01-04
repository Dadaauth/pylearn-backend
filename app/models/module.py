from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import ENUM

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class Module(BaseModel, Base):
    __tablename__ = "modules"

    title = mapped_column(String(60), nullable=False)
    description = mapped_column(String(300))
    status = mapped_column(ENUM("deleted", "draft", "published"), default="draft", nullable=False)
    
    projects = relationship("Project", back_populates="module")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"title", "status"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")