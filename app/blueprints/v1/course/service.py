from app.models.course import Course
from app.models.module import Module
from app.models.project import Project
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound

def icreate_course():
    data = extract_request_data("json")
    if not data.get("title"):
        raise BadRequest("Required field (title) absent in request")
    if not data.get("status"): data["status"] = "published"
    Course(**data).save()

def iretrieve_all_courses():
    tmp = Course.all()
    if not tmp: raise NotFound("No courses found")
    if isinstance(tmp, Course):
        return [tmp.to_dict()]
    
    courses_list = []
    for course in tmp:
        courses_list.append(course.to_dict())
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
    tmp = Project.search(module_id=module_id)
    projects = []
    if isinstance(tmp, Project):
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

def iretrieve_all_course_data(course_id):
    course_with_modules = iretrieve_single_course_with_modules(course_id)
    modules = course_with_modules["modules"]

    for module in modules:
        module['projects'] = retrieve_project_for_module(module.get("id"))

    course_with_modules["modules"] = modules
    return course_with_modules
