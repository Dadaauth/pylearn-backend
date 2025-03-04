from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import ENUM

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys
from app.utils.error_extensions import NotFound


class Cohort(BaseModel, Base):
    __tablename__ = "cohorts"

    # Example Cohort-1
    name = mapped_column(String(60), nullable=False)
    status = mapped_column(ENUM("pending", "in-progress", "completed"), default="pending", nullable=False)
    course_id = mapped_column(ForeignKey("courses.id"), nullable=False)
    start_date = mapped_column(Date, nullable=False)

    next_cohort_id = mapped_column(ForeignKey("cohorts.id"), nullable=True)
    prev_cohort_id = mapped_column(ForeignKey("cohorts.id"), nullable=True)

    next_cohort = relationship("Cohort", remote_side="Cohort.id", foreign_keys=[next_cohort_id])
    prev_cohort = relationship("Cohort", remote_side="Cohort.id", foreign_keys=[prev_cohort_id])
    course = relationship("Course")
    students = relationship("Student", back_populates="cohort")
    mentors = relationship("MentorCohort", back_populates="cohort")

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"name", "course_id", "start_date"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")

        self.insert_cohort_at_correct_node(**kwargs)

    def insert_cohort_at_correct_node(self, **kwargs):
        last_cohort = Cohort.search(course_id=kwargs["course_id"], next_cohort_id=None)

        if last_cohort is None:
            self.save()
            return

        self.prev_cohort_id = last_cohort.id
        self.save()
        last_cohort.next_cohort_id = self.id
        last_cohort.save()

    def sort_cohorts(cohorts):
        """
            Note: This method only works for
                cohorts from the same course
        """
        if cohorts is None or cohorts == []: return cohorts
        if not isinstance(cohorts, list): return cohorts

        # Retrieve the head of the list
        head = None
        for cohort in cohorts:
            if cohort.prev_cohort_id is None:
                head = cohort
                break

            # Also account for if the list does not
            # contain a head cohort but you want to
            # choose the topmost cohort
            is_head = True
            prev_cohort_id = cohort.prev_cohort_id
            for cohort in cohorts:
                if cohort.id == prev_cohort_id:
                    is_head = False
                    break
            if is_head:
                head = cohort
                break

        # sorting process
        tmp = head
        tmp_list = [head]
        while tmp is not None and tmp.cohort_id is not None:
            for cohort in cohorts:
                if cohort.id == tmp.next_cohort_id:
                    tmp_list.append(cohort)
                    tmp = cohort
                    break

        cohorts = tmp_list
        return cohorts