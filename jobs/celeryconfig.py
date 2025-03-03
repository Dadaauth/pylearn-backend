from celery.schedules import crontab


broker = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'
timezone = "Africa/Lagos"
enable_utc = False

beat_schedule = {
    'review-ongoing-projects': {
        'task': 'jobs.tasks.jobs.review_ongoing_projects',
        'schedule': crontab(hour=6, minute=0),
    },
    'release-projects': {
        'task': 'jobs.tasks.jobs.release_projects',
        'schedule': crontab(hour=6, minute=0),
    },
}

task_routes = {
    'jobs.tasks.jobs.review_ongoing_projects': {'queue': 'daily_run'},
    'jobs.tasks.jobs.release_projects': {'queue': 'daily_run'},
    'jobs.tasks.jobs.send_email': {'queue': 'mailing_service'},
},