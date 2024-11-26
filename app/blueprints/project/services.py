import os
from flask_jwt_extended import create_access_token, create_refresh_token, current_user

from app.models.project import Project
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, InternalServerError, UnAuthenticated


def create_new_project():
    data = extract_request_data("json")
    new_project = Project(**data)
    new_project.insert_node_end()

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
    print("\n\n\n")
    print("------------------")
    print("Head => ", project_head)
    print("------------------")
    print("\n\n\n")
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