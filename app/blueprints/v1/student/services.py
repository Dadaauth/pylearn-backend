from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import extract_request_data, retrieve_models_info
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student, Admin
from app.models.module import Module
from app.models.project import AdminProject, CohortProject, StudentProject
from app.models.course import Course

def get_course_and_cohort_id():
    student_id = get_jwt_identity()["id"]
    student = Student.search(id=student_id)
    return student.course_id, student.cohort_id

def get_modules(course_id: str):
    modules = Module.search(course_id=course_id, status="published")
    if not modules:
        return []

    if isinstance(modules, Module):
        modules = [modules.to_dict()]
    elif isinstance(modules, list):
        t_list = []
        for module in modules:
            t_list.append(module.to_dict())
        modules = t_list

    return modules

def append_projects_statuses(projects):
    for project in projects:
        studentProject = StudentProject.search(cohort_project_id=project["id"])
        if not studentProject: continue
        project["status"] = studentProject.status
    return projects

def append_projects_to_modules(modules, cohort_id):
    for module in modules:
        projects = CohortProject.search(cohort_id=cohort_id, module_id=module["id"])
        if not projects:
            module["projects"] = []
            continue

        if isinstance(projects, CohortProject):
            projects = [projects]
        
        projects = retrieve_models_info(projects)
        projects = append_projects_statuses(projects)
        module["projects"] = projects
        
    return modules

def submit_project(project_id, data):
    student = Student.search(id=get_jwt_identity()['id'])
    data["cohort_id"] = student.cohort_id
    data["status"] = "submitted"
    data["student_id"] = student.id
    data["cohort_project_id"] = project_id
    StudentProject(**data).save()

def get_extra_project_details(project):
    studentProject = StudentProject.search(id=project["id"])
    if studentProject:
        project["studentProject"] = studentProject.to_dict()
    author = Admin.search(id=project["author_id"])
    if author:
        project["author"] = author.to_dict()
    return project

def get_project_data(project_id):
    if not project_id: return
    cohortProject = CohortProject.search(id=project_id)
    if not cohortProject: raise NotFound("Project not found")
    cohort_project_dict = cohortProject.to_dict()
    
    studentProject = StudentProject.search(cohort_project_id=cohortProject.id)
    if not studentProject:
        cohort_project_dict["status"] = "released"
    else:
        cohort_project_dict["status"] = studentProject.status

    module = Module.search(id=cohortProject.module_id)
    if module:
        cohort_project_dict["module"] = module.to_dict()
    return cohort_project_dict

def count_completed_modules():
    student_id = get_jwt_identity()["id"]
    student = Student.search(id=student_id)
    all_modules = Module.search(course_id=student.course_id)
    modules_count = Module.count(course_id=student.course_id)
    completed_modules_count = 0
    if not all_modules:
        return {"completed": 0, "all": 0}
    for module in all_modules:
        projects = AdminProject.search(module_id=module.id)
        if isinstance(projects, AdminProject): projects = [projects]
        projects_count = len(projects) if projects else 0
        projects_released = CohortProject.search()

        if not projects or not projects_released: continue
        project_ids = []
        for project in projects_released:
            project_ids.append(project.id)
        completed_projects = StudentProject.count(cohort_project_id=tuple(pid for pid in project_ids),\
            student_id=student_id, cohort_id=student.cohort_id)
        if projects_count == completed_projects:
            completed_modules_count += 1
    return {"completed": completed_modules_count, "all": modules_count}

def count_completed_projects():
    student_id = get_jwt_identity()["id"]
    student = Student.search(id=student_id)
    completed_projects = StudentProject.count(student_id=student_id, cohort_id=student.cohort_id)
    all_projects = AdminProject.count(course_id=student.course_id)
    return {"completed": completed_projects, "all": all_projects}

def ifetch_current_projects():
    student_id = get_jwt_identity()["id"]
    student = Student.search(id=student_id)
    projects = CohortProject.search(cohort_id=student.cohort_id, status=("released", "second-attempt"))

    if not projects: return []

    if isinstance(projects, CohortProject):
        projects = [projects.to_dict()]
    elif isinstance(projects, list):
        projects = retrieve_models_info(projects)

    return projects

def iretrieve_students_with_no_cohort(course_id):
    tmp = Student.search(course_id=course_id, cohort_id=None)
    students = [] 
    if isinstance(tmp, Student):
        students.append(tmp.basic_info())
    elif isinstance(tmp, list):
        for student in tmp:
            students.append(student.basic_info())
    return students

def student_create_new_account():
    data = extract_request_data("json")
    if not (data.get("first_name") and data.get("last_name") and data.get("email") and data.get("course_id")):
        raise BadRequest("Missing required field(s): first_name, last_name, email, course_id")
    
    if Student.search(email=data.get("email")) is not None:
        raise BadRequest("Student Account created Already!")
    
    if not Course.search(id=data.get("course_id")):
        raise BadRequest("Selected Course does not exist!")

    student_details = {
        **data,
        "status": "inactive",
    }
    Student(**student_details).save()