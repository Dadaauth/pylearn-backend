from uuid import uuid4

from sqlalchemy import DateTime, Integer, String, ForeignKey, Text, UniqueConstraint, Float
from sqlalchemy.dialects.mysql import LONGTEXT, ENUM
from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys
from app.utils.error_extensions import NotFound

class BaseProject(BaseModel):
    title = mapped_column(String(300), nullable=False)
    description = mapped_column(String(300))
    markdown_content = mapped_column(LONGTEXT)

    # Nullable, as projects with no module can be assigned under 'misc'
    module_id = mapped_column(ForeignKey("modules.id"))
    author_id = mapped_column(ForeignKey("admins.id"), nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        """
        super().__init__()

        required_keys = {'title', 'author_id', 'course_id'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")

    @classmethod    
    def insert_project_at_correct_node(cls, project, **kwargs):
        # insert Project at the correct node
        if cls.search() is None:
            # list is empty therefore insert as head of the list
            project.prev_project_id = None
            project.next_project_id = None
            project.save()
            return

        prev_project_id = kwargs.get("prev_project_id")
        if not prev_project_id:
            head_project = cls.search(prev_project_id=None)
        
        project.save()
        project.refresh()

        if not prev_project_id:
            # Make first project in list
            head_project.prev_project_id = project.id
            head_project.save()

            project.next_project_id = head_project.id
        else:
            prev_project = cls.search(id=prev_project_id)
            if prev_project is None:
                project.delete()
                raise NotFound("Previous Project Not Found")

            next_p_id = prev_project.next_project_id
            prev_project.next_project_id = project.id
            prev_project.save()
            project.next_project_id = next_p_id

            # Check if the next project exists
            next_project = cls.search(id=next_p_id)
            if next_project:
                next_project.prev_project_id = project.id
                next_project.save()

        project.save()
    
    @classmethod
    def all(cls):
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        projects = super().all()
        return cls.sort_projects(projects)

    @classmethod
    def search(cls, **filters: dict) -> list:
        """
        You need to intercept here because you need
            to sort the projects before you send them
            to the client calling the models API
        """
        projects = super().search(**filters)
        return cls.sort_projects(projects)
    
    @classmethod
    def update(cls, project, **kwargs: dict) -> None:
        """
            You need to intercept here to account for
            updates involving the arrangement of nodes
            in the linked list of projects

            Update a set of attributes in an object.
            :params
                @kwargs: a dictionary of attributes
                        to update
        """
        # update to project ordering
        if project.prev_project_id != kwargs.get("prev_project_id"):
            """
                Code for if the client is trying
                to update the order of the projects
                in the linked list.

            """
            next_project = cls.search(id=project.next_project_id)
            prev_project = cls.search(id=project.prev_project_id)
            new_prev_project = cls.search(id=kwargs.get("prev_project_id"))
            head_project = cls.search(prev_project_id=None)

            # Detach connection from previous spot
            if next_project:
                next_project.prev_project_id = project.prev_project_id
            if prev_project:
                prev_project.next_project_id = project.next_project_id

            project.prev_project_id = None
            project.next_project_id = None

            # Add project to new spot in the list
            if new_prev_project:
                project.prev_project_id = new_prev_project.id
                project.next_project_id = new_prev_project.next_project_id

                if new_prev_project.next_project:
                    new_prev_project.next_project.prev_project_id = project.id

                new_prev_project.next_project_id = project.id
            elif new_prev_project is None and head_project:
                project.next_project_id = head_project.id
                head_project.prev_project_id = project.id

        super().update(**kwargs)

    def sort_projects(projects):
        if projects is None or projects == []: return projects
        if not isinstance(projects, list): return projects

        # Retrieve the head of the list
        head = None
        for project in projects:
            if project.prev_project_id is None:
                head = project
                break

            is_head = True
            prev_project_id = project.prev_project_id
            for project in projects:
                if project.id == prev_project_id:
                    is_head = False
                    break
            if is_head:
                head = project
                break

        # sorting process
        tmp = head
        tmp_list = [head]
        while tmp is not None and tmp.next_project_id is not None:
            for project in projects:
                if project.id == tmp.next_project_id:
                    tmp_list.append(project)
                    tmp = project
                    break

        projects = tmp_list
        return projects

class AdminProject(BaseProject, Base):
    __tablename__ = "admin_projects"

    status = mapped_column(ENUM("deleted", "draft", "published"), default="published", nullable=False)
    # How many days the project will last
    duration_in_days = mapped_column(Integer, nullable=False)
    # How long after the previous project should this project be released?
    # 0 means immediately
    release_range = mapped_column(Integer, nullable=False)
    next_project_id = mapped_column(ForeignKey("admin_projects.id"), nullable=True)
    prev_project_id = mapped_column(ForeignKey("admin_projects.id"), nullable=True)

    next_project = relationship("AdminProject", remote_side="AdminProject.id", foreign_keys=[next_project_id])
    prev_project = relationship("AdminProject", remote_side="AdminProject.id", foreign_keys=[prev_project_id])

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'status'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        super().insert_project_at_correct_node(self, **kwargs)


class CohortProject(BaseProject, Base):
    __tablename__ = "cohort_projects"

    start_date = mapped_column(DateTime, nullable=False)
    end_date = mapped_column(DateTime, nullable=False)
    next_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=True)
    prev_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=True)

    next_project = relationship("CohortProject", remote_side="CohortProject.id", foreign_keys=[next_project_id])
    prev_project = relationship("CohortProject", remote_side="CohortProject.id", foreign_keys=[prev_project_id])

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'start_date', 'end_date'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        super().insert_project_at_correct_node(self, **kwargs)


class StudentProject(BaseModel, Base):
    __tablename__ = "student_projects"
    __table_args__ = (
        UniqueConstraint('student_id', 'cohort_project_id', name='unique_student_id__cohort_project_id'),
    )

    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    cohort_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=False)
    status = mapped_column(ENUM("released", "submitted", "graded", "verified"), default="released", nullable=False)
    submission_file = mapped_column(String(300))
    submitted_on = mapped_column(DateTime)
    assigned_to = mapped_column(ForeignKey("mentors.id"))
    graded_on = mapped_column(DateTime)
    graded_by = mapped_column(ForeignKey("mentors.id"))
    grade = mapped_column(Float)
    feedback = mapped_column(Text)

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"student_id", "cohort_project_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")