from celery.schedules import crontab


broker = 'pyamqp://guest@localhost//'
result_backend = 'rpc://'
timezone = "Africa/Lagos"
enable_utc = False

beat_schedule = {
    'start-cohorts': {
        'task': 'start-cohorts',
        'schedule': crontab(hour=6, minute=0),
    },
    'review-ongoing-projects': {
        'task': 'review-ongoing-projects',
        'schedule': crontab(hour=6, minute=0),
    },
    'release-projects': {
        'task': 'release-projects',
        'schedule': crontab(hour=6, minute=0),
    },
}

task_routes = {
    'review-ongoing-projects': {'queue': 'daily_run'},
    'release-projects': {'queue': 'daily_run'},
    'start-cohorts': {'queue': 'daily_run'},
    'send-transactional-email': {'queue': 'mailing_service'},
    'send-batch-transactional-email': {'queue': 'mailing_service'},
},