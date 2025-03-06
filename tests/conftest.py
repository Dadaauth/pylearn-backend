import os
from datetime import date, timedelta

import pytest


@pytest.fixture
def app():
    from app import create_app
    app = create_app("testing")

    yield app
    # Clean up / reset resources here
    with app.app_context():
        from app.models import storage
        storage.clear_all_tables()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username, password, role):
        return self._client.post(
            '/api/v1/auth/login',
            json={'username': username, 'password': password, 'role': role}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def create_course_and_modules(app):
    from app.models.course import Course
    from app.models.module import Module
    with app.test_request_context():
        app.preprocess_request()
        course = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        course_dict = course.to_dict()
        course.save()
        modules = [
            Module(title="Module 1", course_id=course.id),
            Module(title="Module 2", course_id=course.id)
        ]
        mds = []
        for module in modules:
            mds.append(module.to_dict())
            module.save()
        return course_dict, mds

@pytest.fixture
def create_course(app):
    from app.models.course import Course
    with app.test_request_context():
        app.preprocess_request()
        course = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        course_dict = course.to_dict()
        course.save()
        return course_dict

@pytest.fixture
def create_module(app, create_course):
    from app.models.module import Module
    with app.test_request_context():
        app.preprocess_request()
        course = create_course
        module = Module(title="Module 1", course_id=course["id"])
        module_dict = module.to_dict()
        module.save()
        return course, module_dict

@pytest.fixture
def create_project(app, admin, create_module):
    from app.models.project import AdminProject
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        
        data = {
            "title": "Test Project",
            "module_id": module["id"],
            "author_id": admin.id,
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project = AdminProject(**data)
        project.refresh()
        project_dict = project.to_dict()
        project.save()
        return course, module, project_dict

@pytest.fixture
def create_projects(app, admin, create_module):
    from app.models.project import AdminProject
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        
        data1 = {
            "title": "Test Project",
            "module_id": module["id"],
            "author_id": admin.id,
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        data2 = {
            "title": "Test Project 2",
            "module_id": module["id"],
            "author_id": admin.id,
            "course_id": course["id"],
            "fa_duration": 4,
            "sa_duration": 1,
            "release_range": 4,
            "status": "published",
        }
        projects = [
            AdminProject(**data1),
            AdminProject(**data2)
        ]
        pjts = []
        for project in projects:
            project.refresh()
            pjts.append(project.to_dict())
            project.save()
        return course, module, pjts

@pytest.fixture
def admin(client, app):
    from app.models.user import Admin
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    data = response.json
    with app.test_request_context():
        app.preprocess_request()
        return Admin.search(id=data.get("data")["user"]["id"])

@pytest.fixture
def student(app):
    from app.models.course import Course
    from app.models.cohort import Cohort
    from app.models.user import Admin, Student
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
        student = Student(**data)
        student_dict = student.to_dict()
        student.save()
        return Student.search(id=student_dict["id"])
