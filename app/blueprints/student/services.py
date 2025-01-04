

from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student
from app.models.module import Module
from app.models.project import Project, StudentProject


def ifetch_modules_for_student():
    student_id = get_jwt_identity()["id"]
    mds = Module.all()
    modules = [mod.to_dict() for mod in mds]
    
    for module in modules:
        projects = jfetch_projects(module.get("id"))
        projects_status = []

        if not projects:
            module["status"] = "locked"
            continue

        for project in projects:
            studentProject = StudentProject.search(student_id=student_id, project_id=project.get("id"))
            if studentProject:
                project["status"] = studentProject.status
            else:
                project["status"] = "locked"
            projects_status.append(project["status"])

        # Set the status of modules based on the status of their projects
        if "released" in projects_status:
            module["status"] = "released"

        if all([s == "locked" for s in projects_status]):
            module["status"] = "locked"

        if all([s == "submitted" or s == "graded" or s == "verified"
                for s in projects_status]):
            module["status"] = "completed"

        module["projects"] = projects

    return modules
    

def jfetch_projects(module_id):
    if module_id:
        projects = Project.search(module_id=module_id)
    else:
        projects = Project.all()

    p_list = []

    if projects:
        if isinstance(projects, list):
            for project in projects:
                p_list.append(project.to_dict())
        else:
            p_list = [projects.to_dict()]
    return p_list

def activate_student_account():
    data = extract_request_data("json")
    registration_number = data.get("registration_number")
    if not registration_number:
        raise BadRequest("Missing required field: registration_number")

    student = Student.search(registration_number=registration_number)
    if not student:
        raise NotFound(f"Student with Registration Number {registration_number} not found")
    
    if not (data.get("username") and data.get("password") and data.get("phone")):
        raise BadRequest("Missing required field(s): username, password, phone")

    if student.status == "active":
        raise BadRequest("Account Activated Already!!")

    student.update(**{
        "username": data["username"],
        "password": data["password"],
        "phone": data["phone"],
        "status": "active"
    })
    student_id = student.id
    student.save()
    return student_id
    

def release_first_project(student_id):
    project = Project.search(prev_project_id=None)
    if not project:
        return
    
    StudentProject(
        student_id=student_id,
        project_id=project.id,
        status="released"
    ).save()