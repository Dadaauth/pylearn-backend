from flask import request
from flask_jwt_extended import jwt_required

from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions
from .services import get_modules, append_projects_to_modules, get_project_data, get_extra_project_details
from .services import get_projects, create_project, update_project, get_cohorts, get_mentors_with_assigned_cohorts
from .services import assign_mentor_to_cohorts

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def project_create_page(course_id):
    if request.method == "GET":
        modules = get_modules(course_id)
        projects = get_projects(course_id)
        return format_json_responses(data={"modules": modules, "projects": projects})
    elif request.method == "POST":
        create_project(course_id)
        return format_json_responses(201, message="Resource created successfully!")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def project_edit_page(project_id):
    if request.method == "GET":
        currentProject = get_project_data(project_id)
        modules = get_modules(currentProject["course_id"])
        projects_tmp = get_projects(currentProject["course_id"])

        projects = []
        # remove the current project from the list of projects
        for project in projects_tmp:
            if project['id'] != project_id:
                projects.append(project)

        return format_json_responses(data={"currentProject": currentProject,\
            "modules": modules, "projects": projects})
    elif request.method == "PATCH":
        update_project(project_id)
        return format_json_responses(message="Record update successful!")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def single_project_page(project_id):
    project = get_project_data(project_id)
    project = get_extra_project_details(project)
    next_project = get_project_data(project["next_project_id"])
    prev_project = get_project_data(project["prev_project_id"])
    return format_json_responses(data={"project": project, "next_project": next_project, "prev_project": prev_project})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def adminprojects_page(course_id):
    modules = get_modules(course_id)
    modules = append_projects_to_modules(modules)
    return format_json_responses(data={"modules": modules})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def adminmentors_page():
    if request.method == "GET":
        cohorts = get_cohorts()
        mentors = get_mentors_with_assigned_cohorts()
        return format_json_responses(data={"cohorts": cohorts, "mentors": mentors})
    elif request.method == "PATCH":
        assign_mentor_to_cohorts()
        return format_json_responses(message="Record Updated Successfully")
