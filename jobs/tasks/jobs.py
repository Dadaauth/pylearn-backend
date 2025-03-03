from app import create_app, g
from app.models import storage

from jobs.celery import app
from jobs.tasks.utils.release_projects import release_projects_recursively
from jobs.tasks.utils.release_projects import get_active_cohorts

flask_app = create_app()


@app.task
def review_ongoing_projects():
    # update projects status from released to second-attempt to completed
    ...

@app.task
def release_projects():
    with flask_app.app_context():
        storage.load()
        g.db_storage = storage

        cohorts = get_active_cohorts()
        if not cohorts: return

        for cohort in cohorts:
            release_projects_recursively(cohort)
            # a send_email task can be called here to
            # notify students of their released projects

@app.task
def send_email():
    ...