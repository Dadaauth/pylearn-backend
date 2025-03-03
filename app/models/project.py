from uuid import uuid4

from sqlalchemy import DateTime, Date, Integer, String, ForeignKey, Text, UniqueConstraint, Float
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

    module_id = mapped_column(ForeignKey("modules.id"), nullable=False)
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
    # first attempt duration and second attempt duration
    fa_duration = mapped_column(Integer, nullable=False)
    sa_duration = mapped_column(Integer, nullable=False)
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
        super().__init__(**kwargs)
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'status', 'fa_duration', 'sa_duration', 'release_range'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        self.insert_project_at_correct_node(**kwargs)

    def insert_project_at_correct_node(self, **kwargs):
        # insert Project at the correct node
        if AdminProject.search(course_id=kwargs["course_id"]) is None:
            # list is empty therefore insert as head of the list
            self.prev_project_id = None
            self.next_project_id = None
            self.save()
            return

        prev_project_id = kwargs.get("prev_project_id")
        if not prev_project_id:
            head_project = AdminProject.search(course_id=kwargs["course_id"], prev_project_id=None)
        
        self.save()
        self.refresh()

        if not prev_project_id:
            # Make first project in list
            head_project.prev_project_id = self.id
            head_project.save()

            self.next_project_id = head_project.id
        else:
            prev_project = AdminProject.search(id=prev_project_id)
            if prev_project is None:
                self.delete()
                raise NotFound("Previous Project Not Found")

            next_p_id = prev_project.next_project_id
            prev_project.next_project_id = self.id
            prev_project.save()
            self.next_project_id = next_p_id

            # Check if the next project exists
            next_project = AdminProject.search(id=next_p_id)
            if next_project:
                next_project.prev_project_id = self.id
                next_project.save()

        self.save()

    def update(self, **kwargs: dict) -> None:
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
        if self.prev_project_id != kwargs.get("prev_project_id"):
            """
                Code for if the client is trying
                to update the order of the projects
                in the linked list.

            """
            next_project = AdminProject.search(id=self.next_project_id)
            prev_project = AdminProject.search(id=self.prev_project_id)
            new_prev_project = AdminProject.search(id=kwargs.get("prev_project_id"))
            head_project = AdminProject.search(course_id=self.course_id, prev_project_id=None)

            # Detach connection from previous spot
            if next_project:
                next_project.prev_project_id = self.prev_project_id
            if prev_project:
                prev_project.next_project_id = self.next_project_id

            self.prev_project_id = None
            self.next_project_id = None

            # Add project to new spot in the list
            if new_prev_project:
                self.prev_project_id = new_prev_project.id
                self.next_project_id = new_prev_project.next_project_id

                if new_prev_project.next_project:
                    new_prev_project.next_project.prev_project_id = self.id

                new_prev_project.next_project_id = self.id
            elif new_prev_project is None and head_project:
                self.next_project_id = head_project.id
                head_project.prev_project_id = self.id

        super().update(**kwargs)

class CohortProject(BaseProject, Base):
    __tablename__ = "cohort_projects"

    # first attempt and second attempt start date
    fa_start_date = mapped_column(Date, nullable=False)
    sa_start_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)
    status = mapped_column(ENUM("released", "second-attempt", "completed"), default="released", nullable=False)
    cohort_id = mapped_column(ForeignKey("cohorts.id"), nullable=False)
    # ID of the project in the AdminProject table
    project_pool_id = mapped_column(ForeignKey("admin_projects.id"), nullable=False)
    next_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=True)
    prev_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=True)

    next_project = relationship("CohortProject", remote_side="CohortProject.id", foreign_keys=[next_project_id])
    prev_project = relationship("CohortProject", remote_side="CohortProject.id", foreign_keys=[prev_project_id])

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'project_pool_id', 'fa_start_date', 'sa_start_date', 'end_date', 'cohort_id', 'status'}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        self.insert_project_at_correct_node(**kwargs)

    def insert_project_at_correct_node(self, **kwargs):
        # insert Project at the correct node
        if CohortProject.search(cohort_id=kwargs["cohort_id"]) is None:
            # list is empty therefore insert as head of the list
            self.prev_project_id = None
            self.next_project_id = None
            self.save()
            return

        prev_project_id = kwargs.get("prev_project_id")
        if not prev_project_id:
            head_project = CohortProject.search(cohort_id=kwargs["cohort_id"], prev_project_id=None)
        
        self.save()
        self.refresh()

        if not prev_project_id:
            # Make first project in list
            head_project.prev_project_id = self.id
            head_project.save()

            self.next_project_id = head_project.id
        else:
            prev_project = CohortProject.search(id=prev_project_id)
            if prev_project is None:
                self.delete()
                raise NotFound("Previous Project Not Found")

            next_p_id = prev_project.next_project_id
            prev_project.next_project_id = self.id
            prev_project.save()
            self.next_project_id = next_p_id

            # Check if the next project exists
            next_project = CohortProject.search(id=next_p_id)
            if next_project:
                next_project.prev_project_id = self.id
                next_project.save()

        self.save()

    def update(self, **kwargs: dict) -> None:
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
        if self.prev_project_id != kwargs.get("prev_project_id"):
            """
                Code for if the client is trying
                to update the order of the projects
                in the linked list.

            """
            next_project = CohortProject.search(id=self.next_project_id)
            prev_project = CohortProject.search(id=self.prev_project_id)
            new_prev_project = CohortProject.search(id=kwargs.get("prev_project_id"))
            head_project = CohortProject.search(cohort_id=self.cohort_id, prev_project_id=None)

            # Detach connection from previous spot
            if next_project:
                next_project.prev_project_id = self.prev_project_id
            if prev_project:
                prev_project.next_project_id = self.next_project_id

            self.prev_project_id = None
            self.next_project_id = None

            # Add project to new spot in the list
            if new_prev_project:
                self.prev_project_id = new_prev_project.id
                self.next_project_id = new_prev_project.next_project_id

                if new_prev_project.next_project:
                    new_prev_project.next_project.prev_project_id = self.id

                new_prev_project.next_project_id = self.id
            elif new_prev_project is None and head_project:
                self.next_project_id = head_project.id
                head_project.prev_project_id = self.id

        super().update(**kwargs)


class StudentProject(BaseModel, Base):
    __tablename__ = "student_projects"
    __table_args__ = (
        UniqueConstraint('student_id', 'cohort_project_id', name='unique_student_id__cohort_project_id'),
    )

    cohort_id = mapped_column(ForeignKey("cohorts.id"), nullable=False)
    student_id = mapped_column(ForeignKey("students.id"), nullable=False)
    cohort_project_id = mapped_column(ForeignKey("cohort_projects.id"), nullable=False)
    status = mapped_column(ENUM("submitted", "graded", "verified"), default="submitted", nullable=False)
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

        required_keys = {"status", "cohort_id", "student_id", "cohort_project_id"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")