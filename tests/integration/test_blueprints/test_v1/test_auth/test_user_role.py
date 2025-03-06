"""
Test cases for /api/v1/auth/user/role endpoint
"""
import os
from datetime import date, timedelta


def test_admin_is_logged_in_success(client):
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

    response = client.get('/api/v1/auth/is_logged_in', headers={
        "Authorization": f"Bearer {data.get("data").get("access_token")}"
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("user").get("role") == "admin"
    assert data.get("data").get("user").get("id") is not None
    assert data.get("message") is not None

def test_mentor_is_logged_in_success(app, client):
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

    response = client.get('/api/v1/auth/is_logged_in', headers={
        "Authorization": f"Bearer {data.get("data").get("access_token")}"
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("user").get("role") == "mentor"
    assert data.get("data").get("user").get("id") is not None
    assert data.get("message") is not None

def test_student_is_logged_in_success(app, client):
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

    response = client.get('/api/v1/auth/is_logged_in', headers={
        "Authorization": f"Bearer {data.get("data").get("access_token")}"
    })
    data = response.json
    assert response.status_code == 200
    assert data.get("data").get("user").get("role") == "student"
    assert data.get("data").get("user").get("id") is not None
    assert data.get("message") is not None

def test_is_logged_in_invalid_authentication(client):
    response = client.get('/api/v1/auth/is_logged_in')
    assert response.status_code == 401

def test_is_logged_in_wrong_method(client):
    response = client.post('/api/v1/auth/is_logged_in')
    assert response.status_code == 405