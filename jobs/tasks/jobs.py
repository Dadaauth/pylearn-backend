import os
import json
from datetime import date

import requests

from app import create_app, g
from app.models import storage
from jobs.celery import app
from jobs.tasks.utils.utils import release_projects_recursively
from jobs.tasks.utils.utils import get_active_cohorts, review_projects
from jobs.tasks.utils.utils import notify_students_of_released_projects
from jobs.tasks.utils.utils import get_pending_cohorts


@app.task(name="start-cohorts")
def start_cohorts():
    # change cohorts status when
    # their start dates is reached
    flask_app = create_app()
    with flask_app.app_context():
        g.db_storage = storage
        g.db_session = storage.load_session()

        cohorts = get_pending_cohorts()
        for cohort in cohorts:
            if cohort.start_date < date.today(): continue
            cohort.status = "in-progress"
            cohort.save()
            cohort.refresh()
            released_projects = release_projects_recursively(cohort)
            notify_students_of_released_projects(released_projects, cohort)


@app.task(name="review-ongoing-projects")
def review_ongoing_projects():
    # update projects status from released to second-attempt to completed
    flask_app = create_app()
    with flask_app.app_context():
        g.db_storage = storage
        g.db_session = storage.load_session()

        cohorts = get_active_cohorts()

        for cohort in cohorts:
            review_projects(cohort)

@app.task(name="release-projects")
def release_projects():
    flask_app = create_app()
    with flask_app.app_context():
        g.db_storage = storage
        g.db_session = storage.load_session()

        cohorts = get_active_cohorts()
        if not cohorts: return

        for cohort in cohorts:
            released_projects = release_projects_recursively(cohort)
            notify_students_of_released_projects(released_projects, cohort)

@app.task(name="send-transactional-email")
def send_transactional_email(subject, htmlBody, receipient_email):
    url = "https://api.zeptomail.com/v1.1/email"

    payload = {
        "from": {"address": os.getenv("ZOHO_NOREPLY_EMAIL"), "name": os.getenv("APPLICATION_NAME")},
        "to": [{"email_address": {"address": receipient_email}}],
        "subject": subject,
        "htmlbody": htmlBody
    }
    payload = json.dumps(payload)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': os.getenv("ZOHO_ZEPTOMAIL_MAIL_TOKEN"),
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

@app.task(name="send-batch-transactional-email")
def send_batch_transactional_email(subject, receipients, htmlBody, mergeInfo=None):
    """
    Send transactional emails to multiple users / email accounts. 
        Note: Merge fields are used for dynamic data that needs to be unique
            for each user
    Example Payload:
        subject = "Batch mail Test",
        
        receipients = [
            {
                "email_address": {
                    "address": "paul.s@zfashions.com",
                    "name": "Paul"
                },
                "merge_info" : { 
                    "contact" : "98********" ,
                    "company" : "Z fashions"
                }
            },
            {
                "email_address": {
                    "address": "rebecca@zcorp.com",
                    "name": "Rebecca"
                },
                "merge_info" : { 
                    "contact" : "87********" ,
                    "company" : "Z Inc."
                }
            },
            {
                "email_address": {
                    "address": "george@zfashions.com",
                    "name": "George"
                },
            }
        ]

        htmlbody = "<div><b>This is a sample email.{{contact}} {{company}}</b></div"
        merge_info = {
        "contact" : "87********" ,
        "company" : "Z fashions" }
        }
    """
    url = "https://api.zeptomail.com/v1.1/email/batch"

    payload = {
        "from": {"address": os.getenv("ZOHO_NOREPLY_EMAIL"), "name": os.getenv("APPLICATION_NAME")},
        "to": receipients,
        "subject": subject,
        "htmlbody": htmlBody,
    }
    if mergeInfo:
        payload["merge_info"] = mergeInfo
    payload = json.dumps(payload)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': os.getenv("ZOHO_ZEPTOMAIL_MAIL_TOKEN"),
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)