"""
Test cases for /api/v1/auth/register endpoint
"""
import os
from datetime import date, timedelta


def test_login_admin_success(client):
    """
    GIVEN:
    WHEN:
    THEN:
    """
    client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "test_password",
        "role": "admin",
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("access_token") is not None
    assert data.get("data").get("access_token") != ""
    assert data.get("data").get("refresh_token") is not None
    assert data.get("data").get("refresh_token") != ""
    assert data.get("data").get("first_name") == "Test"
    assert data.get("data").get("last_name") == "Last"
    assert data.get("data").get("email") == "admin1@email.com"
    assert data.get("data").get("username") == "test_admin1"
    assert data.get("data").get("password") is None
    assert data.get("data").get("id") is None
    assert data.get("data").get("user_id") is not None
    assert data.get("data").get("role") == "admin"
    assert data.get("message") is not None
    assert data.get("statusCode") is not None

def test_login_mentor_success(app, client):
    """
    GIVEN:
    WHEN:
    THEN:
    """
    from app.models.user import Mentor
    with app.test_request_context():
        app.preprocess_request()
        data = {
            "email": "mentor@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_mentor1',
        }
        Mentor(**data).save()

    response = client.post("/api/v1/auth/login", json={
        "username": "test_mentor1",
        "password": "test_password",
        "role": "mentor",
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("access_token") is not None
    assert data.get("data").get("access_token") != ""
    assert data.get("data").get("refresh_token") is not None
    assert data.get("data").get("refresh_token") != ""
    assert data.get("data").get("first_name") == "Test"
    assert data.get("data").get("last_name") == "Last"
    assert data.get("data").get("email") == "mentor@email.com"
    assert data.get("data").get("username") == "test_mentor1"
    assert data.get("data").get("password") is None
    assert data.get("data").get("id") is None
    assert data.get("data").get("user_id") is not None
    assert data.get("data").get("role") == "mentor"
    assert data.get("message") is not None
    assert data.get("statusCode") is not None

def test_login_student_success(app, client):
    """
    GIVEN:
    WHEN:
    THEN:
    """
    from app.models.course import Course
    from app.models.cohort import Cohort
    from app.models.user import Student
    with app.test_request_context():
        app.preprocess_request()
        course = Course(title="Software Engineering",
               status="published",
               communication_channel="https://discord.com/invite"
        )
        course_id = course.id
        course.save()
        cohort = Cohort(name="Cohort-1",
               status="pending",
               course_id=course_id,
               start_date=date.today() + timedelta(days=1),
        )
        cohort_id = cohort.id
        cohort.save()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course_id,
            "cohort_id": cohort_id,
        }
        Student(**data).save()

    response = client.post("/api/v1/auth/login", json={
        "username": "test_student1",
        "password": "test_password",
        "role": "student",
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("access_token") is not None
    assert data.get("data").get("access_token") != ""
    assert data.get("data").get("refresh_token") is not None
    assert data.get("data").get("refresh_token") != ""
    assert data.get("data").get("first_name") == "Test"
    assert data.get("data").get("last_name") == "Last"
    assert data.get("data").get("email") == "student@email.com"
    assert data.get("data").get("username") == "test_student1"
    assert data.get("data").get("password") is None
    assert data.get("data").get("id") is None
    assert data.get("data").get("user_id") is not None
    assert data.get("data").get("role") == "student"
    assert data.get("message") is not None
    assert data.get("statusCode") is not None

def test_login_invalid_role(client):
    """
    GIVEN:
    WHEN:
    THEN:
    """
    client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    response1 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "test_password",
        "role": "wrong role",
    })
    response2 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "test_password",
        "role": "",
    })
    response3 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "test_password",
    })
    assert response1.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400

def test_login_credentials_empty_or_missing(client):
    client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response1 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "",
        "role": "admin",
    })
    response2 = client.post("/api/v1/auth/login", json={
        "username": "",
        "password": "test_password",
        "role": "admin",
    })
    response3 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "role": "admin",
    })
    response4 = client.post("/api/v1/auth/login", json={
        "password": "test_password",
        "role": "admin",
    })
    
    assert response1.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400
    assert response4.status_code == 400

def test_login_wrong_username_or_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response1 = client.post("/api/v1/auth/login", json={
        "username": "test_admin2",
        "password": "test_password",
        "role": "admin",
    })
    response2 = client.post("/api/v1/auth/login", json={
        "username": "test_admin1",
        "password": "test_password1",
        "role": "admin",
    })
    assert response1.status_code == 400
    assert response2.status_code == 400

def test_login_inactive_user_status(app, client):
    from app.models.course import Course
    from app.models.cohort import Cohort
    from app.models.user import Student, Mentor
    # create admin account
    client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "status": "inactive",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    # create student account
    with app.test_request_context():
        app.preprocess_request()
        course = Course(title="Software Engineering",
               status="published",
               communication_channel="https://discord.com/invite"
        )
        course_id = course.id
        course.save()
        cohort = Cohort(name="Cohort-1",
               status="pending",
               course_id=course_id,
               start_date=date.today() + timedelta(days=1),
        )
        cohort_id = cohort.id
        cohort.save()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "inactive",
            "course_id": course_id,
            "cohort_id": cohort_id,
        }
        Student(**data).save()
    # create mentor account
    with app.test_request_context():
        app.preprocess_request()
        data = {
            "email": "mentor@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_mentor1',
            "status": "inactive",
        }
        Mentor(**data).save()


    response1 = client.post("/api/v1/auth/login", json={
        "username": "test_admin2",
        "password": "test_password",
        "role": "admin",
    })
    response2 = client.post("/api/v1/auth/login", json={
        "username": "test_student1",
        "password": "test_password",
        "role": "student",
    })
    response3 = client.post("/api/v1/auth/login", json={
        "username": "test_mentor1",
        "password": "test_password",
        "role": "mentor",
    })

    assert response1.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400

def test_login_student_no_cohort(app, client):
    from app.models.course import Course
    from app.models.user import Student
    with app.test_request_context():
        app.preprocess_request()
        course = Course(title="Software Engineering",
               status="published",
               communication_channel="https://discord.com/invite"
        )
        course_id = course.id
        course.save()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "inactive",
            "course_id": course_id,
        }
        Student(**data).save()

    response = client.post("/api/v1/auth/login", json={
        "username": "test_student1",
        "password": "test_password",
        "role": "student",
    })

    assert response.status_code == 400