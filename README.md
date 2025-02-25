# Backend Service for the software engineering learning website by Authority Innovations Hub

## Instructions to Run

Fulfill the following requirements:

* create a .env file at the root of the repository and add the following:
  * DB_CONNECTION_STRING: \
  connection string for a mysql database
  * TEST_DB_CONNECTION_STRING: \
  connection string for a mysql database for testing
  * SECRET_KEY: \
  a string of characters for encrytion operations like cookies
  * ADMIN_REGISTRATION_PASSCODE: \
  code required by client to send when trying to register an account as an admin

Then run:

```python
python run.py
```


Install RabbitMQ on the target machine
Install Celery on the target machine. If possible install as a system-wide package
