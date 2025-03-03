from celery import Celery

app = Celery('jobs',
            include=['jobs.tasks.jobs'])

app.config_from_object("jobs.celeryconfig")

if __name__ == '__main__':
    app.start()