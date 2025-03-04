# Backend Service for the software engineering learning website by Authority Innovations Hub

## Instructions to Run

Fulfill the following requirements:

* create a .env file at the root of the repository and add the following:
  * DB_CONNECTION_STRING: connection string for a mysql database
  * TEST_DB_CONNECTION_STRING: connection string for a mysql database for testing
  * SECRET_KEY: a string of characters for encrytion operations like cookies
  * ADMIN_REGISTRATION_PASSCODE: code required by client to send when trying to register an account as an admin
  * APPLICATION_NAME
  * ZOHO_NOREPLY_EMAIL
  * ZOHO_EMAIL_PASSWORD
  * ZOHO_ZEPTOMAIL_MAIL_TOKEN
  * SUPPORT_EMAIL
  * WEB_DOMAIN

Then run:

```python
python run.py
```

Install RabbitMQ on the target machine
Install Celery on the target machine. If possible install as a system-wide package

## Celery Setup

Celery is our job or task management tool. It is needed to schedule email deliveries, schedule project releases for cohorts and so much more.

Installation in a virtual environment:

```shell
pip install -U celery
```

Make sure celery beat runs as a background process and is restarted automatically in the case of a crash or system reboot

* **!Important!** See Celery and Celery Beat Setup README.md Documentation: [here](/jobs/README.md)

## RabbitMQ Setup

* Install RabbitMQ on ubuntu using the script [install_rabbit_mq_ubuntu](/install_rabbit_mq_ubuntu.sh) provided in the root of the repo. For other platforms see [Downloading and Installing RabbitMQ](https://www.rabbitmq.com/download.html)

* Setup RabbitMQ for Celery using this guide [Celery RabbitMQ Guide](https://docs.celeryq.dev/en/main/getting-started/backends-and-brokers/rabbitmq.html)
