from datetime import datetime, timezone

from flask_jwt_extended import get_jwt_identity

from app.models.module import Module
from app.models.course import Course
from app.models.project import AdminProject, StudentProject, CohortProject
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Admin, Student


def igrade_student_project():
    data = extract_request_data("json")
    mentor_id = get_jwt_identity()["id"]

    if not data.get("student_project_id") or not data.get("grade"):
        raise BadRequest("Required field(s): student_project_id, grade not present")

    studentProject = StudentProject.search(id=data.get("student_project_id"))
    if not studentProject:
        raise NotFound("Student's project not found")
    
    studentProject.status = "graded"
    studentProject.graded_on = datetime.now(timezone.utc)
    studentProject.graded_by = mentor_id
    studentProject.grade = data.get("grade")
    studentProject.feedback = data.get('feedback')
    studentProject.save()

def iretrieve_projects_with_submissions(cohort_id):
    submissions = StudentProject.search(cohort_id=cohort_id, status="submitted")

    projects_with_submissions = []
    projects_with_submissions_registry = []

    if submissions:
        if isinstance(submissions, StudentProject):
            submissions = [submissions]

        for submission in submissions:
            if submission.cohort_project_id in projects_with_submissions_registry:
                continue
            project = CohortProject.search(id=submission.cohort_project_id)
            if not project: continue
            projects_with_submissions_registry.append(project.id)
            projects_with_submissions.append(project.to_dict())

    return projects_with_submissions


def iretrieve_assigned_project_submissions(project_id):
    mentor_id = get_jwt_identity()["id"]
    project = AdminProject.search(id=project_id)
    assigned_pjts = StudentProject.search(status="submitted", project_id=project_id, assigned_to=mentor_id)

    if not assigned_pjts:
        raise NotFound("No submitted projects")

    tmp = []
    if isinstance(assigned_pjts, StudentProject):
        tmp.append(assigned_pjts)
    elif isinstance(assigned_pjts, list):
        for pjt in assigned_pjts:
            tmp.append(pjt)

    assigned_projects = {
        "project": project.to_dict(),
        "data": [],
    }
    for t in tmp:
        student = Student.search(id=t.student_id)
        data = {
            "student": student.to_dict(),
            "student_project": t.to_dict(),
        }
        assigned_projects.get("data").append(data)
    return assigned_projects

def igenerate_project_submission(project_id):
    mentor_id = get_jwt_identity()["id"]
    submitted_projects = StudentProject.search(project_id=project_id, status="submitted", assigned_to=None)
    if not submitted_projects:
        raise NotFound("No Submitted Projects")

    """Check how many projects were found"""
    if isinstance(submitted_projects, StudentProject):
        submitted_projects.assigned_to = mentor_id
        submitted_projects.save()
    elif isinstance(submitted_projects, list):
        submitted_projects[0].assigned_to = mentor_id
        submitted_projects[0].save()

def ifetch_project(project_id):
    project = AdminProject.search(id=project_id)
    if not project:
        raise NotFound(f"Project with ID {project_id} not found")
    
    author = Admin.search(id=project.author_id)
    module = Module.search(id=project.module_id)
    if not author:
        author = "NIL"
    else:
        author = f"{author.first_name} {author.last_name}"

    project = project.to_dict()
    project["author"] = author
    project["module"] = module.title

    return project


def ifetch_projects_for_cohort(course_id):
    module_id = extract_request_data("args").get('module_id')

    if module_id:
        projects = CohortProject.search(module_id=module_id)
    else:
        projects = CohortProject.search(course_id=course_id)

    p_list = []

    if not projects or projects is None:
        raise NotFound("No projects found")

    if isinstance(projects, list):
        for project in projects:
            p_list.append(project.to_dict())
    elif isinstance(projects, CohortProject):
        p_list = [projects.to_dict()]
    return p_list

def ifetch_projects_for_admin(course_id):
    module_id = extract_request_data("args").get('module_id')

    if module_id:
        projects = AdminProject.search(module_id=module_id)
    else:
        projects = AdminProject.search(course_id=course_id)

    p_list = []

    if not projects or projects is None:
        raise NotFound("No projects found")

    if isinstance(projects, list):
        for project in projects:
            p_list.append(project.to_dict())
    elif isinstance(projects, AdminProject):
        p_list = [projects.to_dict()]
    return p_list

def create_new_project():
    data = extract_request_data("json")

    if not data.get("course_id"):
        raise BadRequest("Missing required field: course_id")

    if not Course.search(id=data.get("course_id")):
        raise BadRequest(f"Course with ID: {data.get("course_id")} not found!")

    status = "draft"
    if data.get("mode") == "publish": status = "published"
    data["author_id"] = get_jwt_identity()["id"]
    data["status"] = status
    
    AdminProject(**data).save()

def update_single_project_details(project_id):
    data = extract_request_data("json")
    project = AdminProject.search(id=project_id)
    if project is None or isinstance(project, list):
        raise BadRequest("Project not found or multiple projects found")
    
    status = "draft"
    if data.get("mode") == "publish": status = "published"
    data["status"] = status
    data["author_id"] = get_jwt_identity()["id"]

    project.update(**data)
    project.save()
