
from app.models.cohort import Cohort
from app.models.user import Student
from app.utils.helpers import extract_request_data, has_required_keys
from app.utils.error_extensions import BadRequest, NotFound


def icreate_cohort():
    data = extract_request_data("json")
    valid, values = has_required_keys(data, {'course_id', 'name', 'status'})
    if not valid:
        raise BadRequest(f"Required keys are missing -> {values}")
    
    Cohort(*data).save()

def iget_cohort(cohort_id):
    cohort = Cohort.search(id=cohort_id)
    if not cohort:
        raise NotFound(f"cohort with ID [{cohort_id}] not found!")
    return cohort.to_dict()

def get_students_for_cohort(cohort_id):
    tmp = Student.search(cohort_id=cohort_id)
    students = []
    if isinstance(tmp, Student):
        students.append(tmp.basic_info())
    if isinstance(tmp, list):
        for student in tmp:
            students.append(student.basic_info())
    return students

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