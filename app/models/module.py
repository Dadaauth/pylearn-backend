from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys


class Module(BaseModel, Base):
    __tablename__ = "modules"

    title = mapped_column(String(60), nullable=False)
    description = mapped_column(String(300))
    
    projects = relationship("Project", back_populates="module")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"title"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")