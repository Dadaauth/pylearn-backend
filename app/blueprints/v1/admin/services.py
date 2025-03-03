from flask_jwt_extended import get_jwt_identity

from app.models.project import AdminProject
from app.models.user import Admin, Mentor, MentorCohort
from app.models.cohort import Cohort
from app.models.course import Course
from app.models.module import Module
from app.utils.error_extensions import NotFound, InternalServerError, BadRequest
from app.utils.helpers import retrieve_models_info, extract_request_data

def delete_previously_assigned_cohorts(mentor_id: str):
    previously_assigned = MentorCohort.search(mentor_id=mentor_id)
    if isinstance(previously_assigned, MentorCohort):
        previously_assigned.delete()
    elif isinstance(previously_assigned, list):
        for prv in previously_assigned:
            prv.delete()

def assign_mentor_to_cohorts():
    data = extract_request_data("json")
    mentor_id = data.get("mentor_id")
    cohort_ids = data.get("cohorts")
    if not mentor_id or cohort_ids is None or type(cohort_ids) != list:
        raise BadRequest("mentor_id and cohorts are required")
    if not Mentor.search(id=mentor_id):
        raise NotFound(f"Mentor with ID [{mentor_id}] not found!")

    for cohort_id in cohort_ids:
        if not Cohort.search(id=cohort_id):
            raise NotFound(f"Cohort with ID [{cohort_id}] not found!")

    delete_previously_assigned_cohorts(mentor_id)

    for cohort_id in cohort_ids:
        if not MentorCohort.search(mentor_id=mentor_id, cohort_id=cohort_id):
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort_id).save()

def get_mentors_with_assigned_cohorts():
    mentors = Mentor.all()
    if not mentors: return []

    if isinstance(mentors, Mentor): mentors = [mentors]
    
    mentors_main = []
    for mentor in mentors:
        cohorts = []
        for cohort in mentor.cohorts:
            cht = Cohort.search(id=cohort.cohort_id)
            if not cht: continue
            cohorts.append(cht)
        cohorts = append_course_to_cohorts(cohorts)
        mentor = mentor.to_dict()
        mentor["cohorts"] = cohorts
        del mentor["password"]
        mentors_main.append(mentor)

    return mentors_main

def append_course_to_cohorts(cohorts):
    chts = []
    for cohort in cohorts:
        tmp = {
            **(cohort.to_dict()),
            "course": cohort.course.to_dict()
        }
        chts.append(tmp)
    return chts

def get_cohorts():
    cohorts = Cohort.all()
    if not cohorts: return []
    
    if isinstance(cohorts, Cohort): cohorts = [cohorts]

    cohorts = append_course_to_cohorts(cohorts)
    return cohorts

def update_project(project_id):
    data = extract_request_data("json")
    pjt = AdminProject.search(id=project_id)
    if not pjt: raise NotFound("Project not found!")
    if isinstance(pjt, list): raise InternalServerError(f"Lots of projects with ID [{project_id}] found")

    pjt.update(**data)
    pjt.save()

def create_project(course_id):
    data = extract_request_data("json")
    data["course_id"] = course_id
    data["author_id"] = get_jwt_identity()["id"]
    data["status"] = "published"
    AdminProject(**data).save()

def get_projects(course_id: str):
    projects = AdminProject.search(course_id=course_id)
    if not projects: return []
    
    if isinstance(projects, AdminProject):
        projects = [projects]
    
    projects = AdminProject.sort_projects(projects)
    p_list = []
    for project in projects:
        p_list.append(project.to_dict())
    return p_list

def get_extra_project_details(project):
    author = Admin.search(id=project["author_id"])
    if author:
        project["author"] = author.to_dict()
    return project

def get_project_data(project_id):
    if not project_id: return
    project = AdminProject.search(id=project_id)
    if not project: raise NotFound("Project not found")
    project_dict = project.to_dict()

    module = Module.search(id=project.module_id)
    if module:
        project_dict["module"] = module.to_dict()
    return project_dict

def get_modules(course_id: str):
    modules = Module.search(course_id=course_id)
    if not modules:
        return []

    if isinstance(modules, Module):
        modules = [modules.to_dict()]
    elif isinstance(modules, list):
        modules = retrieve_models_info(modules)

    return modules

def append_projects_to_modules(modules):
    for module in modules:
        projects = AdminProject.search(module_id=module["id"])
        if not projects:
            module["projects"] = []
            continue

        if isinstance(projects, AdminProject):
            projects = [projects]

        projects = retrieve_models_info(projects)
        module["projects"] = projects

    return modules