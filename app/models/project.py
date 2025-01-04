from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.mysql import LONGTEXT, ENUM
from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys
from app.utils.error_extensions import NotFound

class Project(BaseModel, Base):
    __tablename__ = "projects"

    title = mapped_column(String(300), nullable=False)
    description = mapped_column(String(300))
    markdown_content = mapped_column(LONGTEXT)
    status = mapped_column(ENUM("deleted", "draft", "published"), default="draft", nullable=False)

    module_id = mapped_column(ForeignKey("modules.id"), nullable=False)
    author_id = mapped_column(ForeignKey("admins.id"), nullable=False)

    next_project_id = mapped_column(ForeignKey("projects.id"), nullable=True)
    prev_project_id = mapped_column(ForeignKey("projects.id"), nullable=True)

    module = relationship("Module", back_populates="projects")
    author = relationship("Admin")

    next_project = relationship("Project", remote_side="Project.id", foreign_keys=[next_project_id])
    prev_project = relationship("Project", remote_side="Project.id", foreign_keys=[prev_project_id])

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'title', 'author_id', 'module_id', 'status'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        # insert Project at the correct node
        if Project.count() == 0:
            # insert as head of the list
            self.prev_project_id = None
            self.next_project_id = None
            return
        
        self.save()
        self.refresh()

        prev_project_id = kwargs.get("prev_project_id")
        if not prev_project_id:
            # Make first project in list
            head_project = Project.search(prev_project_id=None)
            head_project.prev_project_id = self.id
            head_project.save() # Add project to session for saving

            self.next_project_id = head_project.id
        else:
            prev_project = Project.search(id=prev_project_id)
            if prev_project is None:
                raise NotFound("Previous Project Not Found")
            next_p_id = prev_project.next_project_id
            prev_project.next_project_id = self.id
            prev_project.save()
            self.next_project_id = next_p_id

            # Check if the next project exists
            next_project = Project.search(id=next_p_id)
            if next_project:
                next_project.prev_project_id = self.id
                next_project.save()

    @classmethod
    def all():
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        return super().all()

    @classmethod
    def search(cls, **filters: dict) -> list:
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        return super().search(**filters)


class StudentProject(BaseModel, Base):
    __tablename__ = "student_projects"

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    project_id = mapped_column(ForeignKey("projects.id"), nullable=False)
    status = mapped_column(ENUM("released", "submitted", "graded", "verified"), default="released", nullable=False)
    submission_file = mapped_column(String(300))
    submitted_on = mapped_column(DateTime)
    graded_on = mapped_column(DateTime)
    graded_by = mapped_column(ForeignKey("admins.id"))
    grade = mapped_column(Integer)
    feedback = mapped_column(Text)

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "project_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")