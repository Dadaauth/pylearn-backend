from flask_jwt_extended import get_jwt_identity

from app.models.module import Module
from app.models.project import Project, StudentProject
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound

def iupdate_module(module_id):
    data = extract_request_data("json")
    to_update =  {
        "title": data.get("title"),
        "description": data.get("description"),
        "status": data.get("status")
    }
    module = Module.search(id=module_id)
    if not module:
        raise NotFound(f"Module with ID {module_id} not found")
    module.update(**to_update)
    module.save()

def ifetch_modules():
    mds = Module.all()
    return [mod.to_dict() for mod in mds]

def icreate_module():
    data = extract_request_data("json")
    if not data.get("title"):
        raise BadRequest("Required field(s) not present: title")

    Module(**data).save()

def fetch_projects():
    module_id = extract_request_data("args").get('module_id')

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

def create_new_project():
    data = extract_request_data("json")

    # fetch status, module_id, author_id, and prev_project_id
    status = "draft"
    if data.get("mode") == "publish": status = "published"
    data["author_id"] = get_jwt_identity()["id"]
    data["status"] = status
    
    Project(**data).save()

def fetch_project_details_single(project_id):
    project = Project.search(id=project_id)
    if not project:
        raise NotFound(f"Project with ID {project_id} not found")
    
    return project.to_dict()

def update_single_project_details(project_id):
    data = extract_request_data("json")
    project = Project.search(id=project_id)
    if project is None or isinstance(project, list):
        raise BadRequest("Project not found or multiple projects found")
    
    status = "draft"
    if data.get("mode") == "publish": status = "published"
    data["status"] = status
    data["author_id"] = get_jwt_identity()["id"]

    project.update(**data)
    project.save()














def _retrieve_projects_status():
    data = extract_request_data("json")
    projects_ids = data.get("projects")
    student_id = data.get("student_id")
    statuses = []
    for p_id in projects_ids:
        student_project = StudentProject.search(student_id=student_id, project_id=p_id)

        if student_project and not isinstance(student_project, list):
            statuses.append({
                "id": p_id,
                "status": student_project.status,
            })
        else:
            statuses.append({
                "id": p_id,
                "status": "unreleased",
            })
    return {"statuses": statuses}

def mark_a_project_as_done():
    data = extract_request_data("json")
    student_id = data.get("student_id")
    project_id = data.get("project_id")

    project = Project.search(id=project_id)

    student_project = StudentProject.search(project_id=project_id, student_id=student_id)
    if student_project is not None and not isinstance(student_project, list):
        student_project.status = "completed"
        student_project.save()
    else:
        if project and not isinstance(project, list):
            student_project = StudentProject(student_id=student_id, project_id=project_id, status="completed")
            student_project.save()
        else:
            raise BadRequest(f"Project does not exist or there are multiple entries for project with id {project_id}")

    if project.next_project:
        if not StudentProject.search(student_id=student_id, project_id=project.next_project_id):
            new_student_project = StudentProject(student_id=student_id, project_id=project.next_project_id, status="pending")
            new_student_project.save()

def sort_projects(projects):
    temp_1 = {}
    p_list = []

    # Retrieve the head of the linked list
    project_head = get_project_head(projects)
    if project_head is None: return []
    p_list.append(project_head)

    # Add the projects to a dictionary
    #   for easier retrieval during sorting
    for project in projects:
        if project.id != project_head.id:
            temp_1[project.id] = project

    # retrieve the next project from the
    # dictionary based on the next_project_id value
    temp_2 = project_head
    while temp_2.next_project_id is not None:
        p_id = temp_2.next_project_id
        temp_2 = temp_1.get(p_id)
        p_list.append(temp_2)
        del temp_1[p_id]

    # Append the remaining unorganized projects to the returned output
    for value in temp_1.values():
        p_list.append(value)

    return p_list

def get_project_head(projects):
    for project in projects:
        if project.prev_project_id == None:
            return project
    return None