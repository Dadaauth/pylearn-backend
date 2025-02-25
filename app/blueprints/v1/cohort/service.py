from flask import request

from app.models.cohort import Cohort
from app.models.course import Course
from app.models.user import Student, MentorCohort, Mentor
from app.utils.helpers import extract_request_data, has_required_keys
from app.utils.error_extensions import BadRequest, NotFound


def icreate_cohort():
    data = extract_request_data("json")
    valid, values = has_required_keys(data, {'course_id', 'name'})
    if not data.get("status"):
        data["status"] = "pending"
    if not valid:
        raise BadRequest(f"Required keys are missing -> {values}")
    
    Cohort(**data).save()

def iget_cohort(cohort_id):
    cohort = Cohort.search(id=cohort_id)
    if not cohort:
        raise NotFound(f"cohort with ID [{cohort_id}] not found!")
    
    cohort_dict =  cohort.to_dict()
    course = Course.search(id=cohort_dict["course_id"])
    if not course:
        raise NotFound(f"Cohort is not assigned a course yet!")
    cohort_dict["course"] = course.to_dict()
    return cohort_dict

def iget_all_cohorts():
    tmp = Cohort.all()
    cohorts = []

    if not tmp:
        raise NotFound("No Cohorts found!")
    if isinstance(tmp, Cohort):
        course = Course.search(id=tmp.course_id)
        tmp = tmp.to_dict()
        tmp["course"] = course.to_dict()
        cohorts.append(tmp)
    if isinstance(tmp, list):
        for cohort in tmp:
            course = Course.search(id=cohort.course_id)
            cohort = cohort.to_dict()
            cohort["course"] = course.to_dict()
            cohorts.append(cohort)
    return cohorts

def get_students_for_cohort(cohort_id):
    tmp = Student.search(cohort_id=cohort_id)
    students = []
    if isinstance(tmp, Student):
        students.append(tmp.basic_info())
    if isinstance(tmp, list):
        for student in tmp:
            students.append(student.basic_info())
    return students

def iadd_students_to_cohort(cohort_id):
    student_ids = extract_request_data("form")[0].getlist("student_ids")
    print(student_ids)
    for student_id in student_ids:
        student = Student.search(id=student_id)
        if student:
            student.cohort_id = cohort_id
            student.status = "active"
            student.save()

def iget_cohort_students(cohort_id):
    cohort = iget_cohort(cohort_id)
    cohort["students"] = get_students_for_cohort(cohort_id)
    return cohort

def iupdate_cohort(cohort_id):
    data = extract_request_data("json")
    if data.get("id"):
        del data["id"]

    cohort = Cohort.search(id=cohort_id)
    if not cohort:
        raise NotFound(f"Cohort with ID [{cohort_id}] not found!")
    cohort.update(**data)
    cohort.save()

def idelete_cohort(cohort_id):
    cohort = Cohort.search(id=cohort_id)
    if not cohort:
        raise NotFound(f"Cohort with ID [{cohort_id}] not found!")
    cohort.delete()

def delete_previously_assigned_cohorts(mentor_id: str):
    previously_assigned = MentorCohort.search(mentor_id=mentor_id)
    if isinstance(previously_assigned, MentorCohort):
        previously_assigned.delete()
    elif isinstance(previously_assigned, list):
        for prv in previously_assigned:
            prv.delete()

def iassign_mentor_to_cohorts():
    data = extract_request_data("json")
    mentor_id = data.get("mentor_id")
    cohort_ids = data.get("cohorts")
    if not mentor_id or cohort_ids is None or type(cohort_ids) != list:
        raise BadRequest("mentor_id and cohorts are required")
    if not Mentor.search(id=mentor_id):
        raise NotFound(f"Mentor with ID [{mentor_id}] not found!")

    delete_previously_assigned_cohorts(mentor_id)

    for cohort_id in cohort_ids:
        if not Cohort.search(id=cohort_id):
            raise NotFound(f"Cohort with ID [{cohort_id}] not found!")
        if not MentorCohort.search(mentor_id=mentor_id, cohort_id=cohort_id):
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort_id).save()

def iremove_mentor_from_cohorts():
    data = extract_request_data("json")
    mentor_id = data.get("mentor_id")
    cohort_ids = data.get("cohort_ids")
    if not mentor_id or not cohort_ids:
        raise BadRequest("mentor_id and cohort_ids are required")
    if not Mentor.search(id=mentor_id):
        raise NotFound(f"Mentor with ID [{mentor_id}] not found!")

    for cohort_id in cohort_ids:
        if not Cohort.search(id=cohort_id):
            raise NotFound(f"Cohort with ID [{cohort_id}] not found!")
        mentor_cohort = MentorCohort.search(mentor_id=mentor_id, cohort_id=cohort_id)
        if mentor_cohort:
            mentor_cohort.delete()