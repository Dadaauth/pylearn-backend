from app.models.user import Student
from app.models.course import Course
from app.models.cohort import Cohort
from app.models.module import Module
from app.models.project import AdminProject, CohortProject, StudentProject
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound

def icreate_course():
    data = extract_request_data("json")
    if not data.get("title", "communication_channel"):
        raise BadRequest("Required field(s) (title or communication_channel) absent in request")
    if not data.get("status"): data["status"] = "published"
    Course(**data).save()

def iretrieve_all_courses():
    tmp = Course.all()
    if not tmp: raise NotFound("No courses found")
    if isinstance(tmp, Course):
        course_dict = tmp.to_dict()
        course_dict["cohorts"] = retrieve_cohorts_for_course(tmp.id)
        return [course_dict]
    
    courses_list = []
    for course in tmp:
        course_dict = course.to_dict()
        course_dict["cohorts"] = retrieve_cohorts_for_course(course.id)
        courses_list.append(course_dict)
    return courses_list

def iretrieve_single_course(course_id):
    course = Course.search(id=course_id)
    if not course:
        raise NotFound(f"No course with id {course_id} found!")
    return course.to_dict()

def iretrieve_single_course_with_modules(course_id):
    course = Course.search(id=course_id)
    if not course:
        raise NotFound(f"No course with id {course_id} found!")
    
    course = course.to_dict()
    course_modules = []

    tmp = Module.search(course_id=course_id)
    if isinstance(tmp, Module):
        course_modules.append(tmp.to_dict())
    if isinstance(tmp, list):
        for module in tmp:
            course_modules.append(module.to_dict())
    
    course["modules"] = course_modules
    return course

def retrieve_project_for_module(module_id):
    tmp = AdminProject.search(module_id=module_id)
    projects = []
    if isinstance(tmp, AdminProject):
        projects.append(tmp.to_dict())
    if isinstance(tmp, list):
        for project in tmp:
            projects.append(project.to_dict())
    return projects

def iupdate_course(course_id):
    data = extract_request_data("json")
    if data.get("id"):
        del data["id"]

    course = Course.search(id=course_id)
    if not course:
        raise NotFound(f"Course with ID [{course_id}] not found!")
    course.update(**data)
    course.save()

def idelete_course(course_id):
    course = Course.search(id=course_id)
    if not course:
        raise NotFound(f"Course with ID [{course_id}] not found!")
    course.delete()

def retrieve_cohorts_for_course(course_id):
    tmp = Cohort.search(course_id=course_id)
    cohorts = []
    if isinstance(tmp, Cohort):
        cohort_dict = tmp.to_dict()
        cohort_dict["students"] = Student.count(cohort_id=tmp.id)
        cohorts.append(cohort_dict)
    if isinstance(tmp, list):
        for cohort in tmp:
            cohort_dict = cohort.to_dict()
            cohort_dict["students"] = Student.count(cohort_id=cohort.id)
            cohorts.append(cohort_dict)
    return cohorts

def iretrieve_all_course_data(course_id):
    course = iretrieve_single_course_with_modules(course_id)
    modules = course["modules"]

    for module in modules:
        module['projects'] = retrieve_project_for_module(module.get("id"))

    course["modules"] = modules
    course["cohorts"] = retrieve_cohorts_for_course(course_id)
    
    return course
