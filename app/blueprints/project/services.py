import os
from flask_jwt_extended import create_access_token, create_refresh_token, current_user

from app.models.project import Project, StudentProject
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, InternalServerError, UnAuthenticated, NotFound

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
        new_student_project = StudentProject(student_id=student_id, project_id=project.next_project_id, status="pending")
        new_student_project.save()

def update_single_project_details(id):
    data = extract_request_data("json")
    project = Project.search(id=id)
    if project is None or isinstance(project, list):
        raise BadRequest("Project not found or multiple projects found")
    project.update(**data)
    project.save()

def create_new_project():
    data = extract_request_data("json")
    new_project = Project(**data)
    new_project.insert_node_end()

def fetch_project_details_single():
    args = extract_request_data("args")
    filter = args.get('q')
    p_id = args.get("id")
    project = Project.search(id=p_id)
    if not project:
        raise NotFound(f"Project with id {p_id} not found!")
    return {"project": retrieve_model_info(project, filter.split(","))}
    # Add search for the staus of the project if the student has completed it.


def fetch_project_details():
    filter = extract_request_data("args").get('q')
    projects = Project.all()
    p_list = []
    projects = sort_projects(projects)

    for project in projects:
        p_list.append(retrieve_model_info(project, filter.split(",")))
    return p_list

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