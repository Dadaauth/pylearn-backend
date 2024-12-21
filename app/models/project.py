from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.mysql import LONGTEXT, ENUM
from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys

class Project(BaseModel, Base):
    __tablename__ = "projects"

    title = mapped_column(String(100), nullable=False)
    description = mapped_column(String(300))
    markdown_content = mapped_column(LONGTEXT)

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

        required_keys = {'title', 'description', 'content'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")

    @classmethod
    def all():
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        return super().all()

    @classmethod
    def search(**filters: dict) -> list:
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        return super().search(filters)

    def remap_node_to_index(self, index):
        """
        Method used for remapping projects order in the linked list.
        Should be used for remapping only and not for assigning a
        new project not yet in the list

        arguments:
            index: a Project instance that comes before the new `self` position
                    Value is None if remapping to `head` (beginning of the list)
        """

        # Rearrange relationship among surrounding projects in previous project position
        if self.prev_project_id is not None:
            self.prev_project.next_project_id = self.next_project_id
        if self.next_project_id is not None:
            self.next_project.prev_project_id = self.id

        # If remapping project to `head` (beginning of list)
        if index is None:
            head_project = Project.search(prev_project_id=None)
            head_project.prev_project_id = self.id
            self.prev_project_id = None
            self.next_project_id = head_project.id

        # Assign new location to project
        self.prev_project_id = index.id
        self.next_project_id = index.next_project_id
        if index.next_project_id is not None:
            index.next_project.prev_project_id = self.id
        index.next_project_id = self.id

    def insert_node_end(self):
        """
        Used for assigning a new project not yet added to
        the linked list (to the end of the list).
        """
        # get the last node
        project = Project.search(next_project_id=None)
        if project is not None and isinstance(project, Project):
            self.prev_project_id = project.id
            self.save()
            project.next_project_id = self.id
            project.save()
        else:
            self.save()


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