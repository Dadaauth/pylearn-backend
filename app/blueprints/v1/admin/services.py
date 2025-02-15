from datetime import datetime, timezone

from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import extract_request_data, retrieve_model_info
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student, Admin
from app.models.project import StudentProject, Project
from app.models.module import Module

def igrade_student_project():
    data = extract_request_data("json")
    admin_id = get_jwt_identity()["id"]

    if not data.get("student_project_id") or not data.get("grade"):
        raise BadRequest("Required field(s): student_project_id, grade not present")

    studentProject = StudentProject.search(id=data.get("student_project_id"))
    if not studentProject:
        raise NotFound("Student's project not found")
    
    studentProject.status = "graded"
    studentProject.graded_on = datetime.now(timezone.utc)
    studentProject.graded_by = admin_id
    studentProject.grade = data.get("grade")
    studentProject.feedback = data.get('feedback')
    studentProject.save()

def iretrieve_assigned_project_submissions(project_id):
    admin_id = get_jwt_identity()["id"]
    project = Project.search(id=project_id)
    assigned_pjts = StudentProject.search(status="submitted", project_id=project_id, assigned_to=admin_id)

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

def iretrieve_projects_with_submissions():
    submissions = StudentProject.search(status="submitted")
    if not submissions:
        raise NotFound("No Submitted Projects Found")

    """Check how many projects were found"""
    if isinstance(submissions, StudentProject):
        submissions = [submissions]

    projects_with_submissions = []
    projects_with_submissions_registry = []
    for submission in submissions:
        if submission.project_id in projects_with_submissions_registry:
            continue
        project = Project.search(id=submission.project_id)
        if not Project: continue
        projects_with_submissions_registry.append(project.id)
        projects_with_submissions.append(project.to_dict())

    return projects_with_submissions
