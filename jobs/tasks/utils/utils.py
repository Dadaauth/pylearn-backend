from datetime import date, timedelta

from app.models.project import AdminProject, CohortProject
from app.models.course import Course
from app.models.cohort import Cohort


def update_project_status(pjt: CohortProject):
    today = date.today()
    if pjt.sa_start_date <= today:
        pjt.update(status='second-attempt')
    if pjt.end_date <= today:
        pjt.update(status='completed')
    pjt.save()

def review_projects(cohort: Cohort):
    cohort_projects = CohortProject.search(cohort_id=cohort.id, status=('released', 'second-attempt'))
    if not cohort_projects: return
    
    if isinstance(cohort_projects, CohortProject): cohort_projects = [cohort_projects]

    for pjt in cohort_projects:
        update_project_status(pjt)

def get_active_cohorts():
    return Cohort.search(status="in-progress")

def release_first_project_for_cohort(cohort: Cohort):
    # Retrieve the first project in the course
    project = AdminProject.search(course_id=cohort.course_id, status="published", prev_project_id=None)
    if not project: return

    release_project_for_cohort(project, cohort)


def release_projects_recursively(cohort: Cohort):
    # release first project for cohort if there are no previously released projects
    cohort_projects = CohortProject.search(cohort_id=cohort.id)
    if not cohort_projects:
        release_first_project_for_cohort(cohort)
    
    # get the last released project
    lr_project = CohortProject.search(cohort_id=cohort.id, next_project_id=None)
    if not lr_project: return
    if not isinstance(lr_project, CohortProject): return

    pool_project = AdminProject.search(id=lr_project.project_pool_id)
    next_project = pool_project.next_project
    if not next_project: return

    next_project_release_date = lr_project.fa_start_date + timedelta(days=next_project.release_range)
    while next_project and next_project_release_date == date.today():
        release_project_for_cohort(next_project, cohort)
        lr_project = next_project
        next_project = lr_project.next_project
        if next_project:
            next_project_release_date = lr_project.fa_start_date + timedelta(days=next_project.release_range)


def release_project_for_cohort(project: AdminProject, cohort: Cohort):
    project_dict = project.to_dict()

    
    # Add attributes needed by CohortProject
    project_dict["project_pool_id"] = project_dict["id"]
    project_dict["cohort_id"] = cohort.id
    project_dict["status"] = "released"
    project_dict['fa_start_date'] = date.today()
    project_dict['sa_start_date'] = date.today() + timedelta(days=int(project_dict["fa_duration"]))
    project_dict['end_date'] = project_dict['sa_start_date'] + timedelta(days=int(project_dict["sa_duration"]))
    project_dict['prev_project_id'] = None
    project_dict['next_project_id'] = None
    
    # Remove attributes not needed by CohortProject
    del project_dict["id"]
    del project_dict["created_at"]
    del project_dict["updated_at"]
    del project_dict["fa_duration"]
    del project_dict["sa_duration"]
    del project_dict["release_range"]
    
    
    last_project = CohortProject.search(cohort_id=cohort.id, next_project_id=None)
    # Create a new CohortProject instance
    new_project = CohortProject(**project_dict)
    new_project.save()
    new_project.refresh()
    if last_project:
        last_project.next_project = new_project.id
        new_project.prev_project_id = last_project.id
        last_project.save()
        new_project.save()