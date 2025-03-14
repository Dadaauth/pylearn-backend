"""
Test cases for /api/v1/student/projects GET endpoint
"""
from datetime import date, datetime, timezone, timedelta


def test_student_get_all_projects_success(app, client, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import CohortProject, StudentProject, AdminProject
        from app.models.cohort import Cohort
        from app.models.user import Student
        from app.models.module import Module
        course, module, projects = create_projects
        # create multiple modules
        module2 = Module(
            title="Module 2",
            status="published",
            course_id=course['id'],
        )
        module2.save()
        module2.refresh()
        data = {
            "title": "Test Project",
            "module_id": module2.id,
            "author_id": projects[0]['author_id'],
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project = AdminProject(**data)
        project.refresh()
        projects.append(project.to_dict())
        project.save()
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=23),
        )
        cohort.save()
        cohort.refresh()
        cohort_projects = []
        for project in projects:
            cohortProject = CohortProject(
                title=project['title'],
                module_id=project['module_id'],
                author_id=project['author_id'],
                course_id=project['course_id'],
                fa_start_date=date.today() - timedelta(days=4),
                sa_start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
                status="second-attempt",
                cohort_id=cohort.id,
                project_pool_id=project['id'],
            )
            cohortProject.save()
            cohortProject.refresh()
            cohort_projects.append(cohortProject.to_dict())
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course['id'],
            "cohort_id": cohort.id,
        }
        student = Student(**data)
        student.save()
        student.refresh()
        StudentProject(
            cohort_id=cohort.id,
            student_id=student.id,
            cohort_project_id=cohort_projects[0]['id'],
            status="submitted",
            submission_file="https://google.com",
            submitted_on=datetime.now(timezone.utc),
        ).save()
        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.get("/api/v1/student/projects", headers={
            "Authorization": f"Bearer {token}"
        })
        data = resp.json

        assert resp.status_code == 200
        assert type(data['data']['modules']) == list
        assert len(data['data']['modules']) == 2
        assert type(data['data']['modules'][0]['projects']) == list
        assert len(data['data']['modules'][0]['projects']) == 2 or len(data['data']['modules'][0]['projects']) == 1
        assert type(data['data']['modules'][1]['projects']) == list
        assert len(data['data']['modules'][1]['projects']) == 1 or len(data['data']['modules'][1]['projects']) == 2

def test_student_get_all_projects_user_logged_out(app, client, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import CohortProject, StudentProject, AdminProject
        from app.models.cohort import Cohort
        from app.models.user import Student
        from app.models.module import Module
        course, module, projects = create_projects
        # create multiple modules
        module2 = Module(
            title="Module 2",
            status="published",
            course_id=course['id'],
        )
        module2.save()
        module2.refresh()
        data = {
            "title": "Test Project",
            "module_id": module2.id,
            "author_id": projects[0]['author_id'],
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project = AdminProject(**data)
        project.refresh()
        projects.append(project.to_dict())
        project.save()
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=23),
        )
        cohort.save()
        cohort.refresh()
        cohort_projects = []
        for project in projects:
            cohortProject = CohortProject(
                title=project['title'],
                module_id=project['module_id'],
                author_id=project['author_id'],
                course_id=project['course_id'],
                fa_start_date=date.today() - timedelta(days=4),
                sa_start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
                status="second-attempt",
                cohort_id=cohort.id,
                project_pool_id=project['id'],
            )
            cohortProject.save()
            cohortProject.refresh()
            cohort_projects.append(cohortProject.to_dict())
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course['id'],
            "cohort_id": cohort.id,
        }
        student = Student(**data)
        student.save()
        student.refresh()
        StudentProject(
            cohort_id=cohort.id,
            student_id=student.id,
            cohort_project_id=cohort_projects[0]['id'],
            status="submitted",
            submission_file="https://google.com",
            submitted_on=datetime.now(timezone.utc),
        ).save()
        resp = client.get("/api/v1/student/projects")
        data = resp.json

        assert resp.status_code == 401
        assert data.get("data") is None

def test_student_get_all_projects_one_module_no_projects(app, client, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.cohort import Cohort
        from app.models.user import Student
        course, module, projects = create_projects
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=23),
        )
        cohort.save()
        cohort.refresh()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course['id'],
            "cohort_id": cohort.id,
        }
        student = Student(**data)
        student.save()
        student.refresh()

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.get("/api/v1/student/projects", headers={
            "Authorization": f"Bearer {token}"
        })
        data = resp.json

        assert resp.status_code == 200
        assert type(data['data']['modules']) == list
        assert len(data['data']['modules']) == 1
        assert type(data['data']['modules'][0]['projects']) == list
        assert len(data['data']['modules'][0]['projects']) == 0

def test_student_get_all_projects_one_module_one_project(app, client, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import CohortProject, StudentProject
        from app.models.cohort import Cohort
        from app.models.user import Student
        course, module, project = create_project

        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=23),
        )
        cohort.save()
        cohort.refresh()
        cohortProject = CohortProject(
            title=project['title'],
            module_id=project['module_id'],
            author_id=project['author_id'],
            course_id=project['course_id'],
            fa_start_date=date.today() - timedelta(days=4),
            sa_start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
            status="second-attempt",
            cohort_id=cohort.id,
            project_pool_id=project['id'],
        )
        cohortProject.save()
        cohortProject.refresh()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course['id'],
            "cohort_id": cohort.id,
        }
        student = Student(**data)
        student.save()
        student.refresh()
        StudentProject(
            cohort_id=cohort.id,
            student_id=student.id,
            cohort_project_id=cohortProject.id,
            status="submitted",
            submission_file="https://google.com",
            submitted_on=datetime.now(timezone.utc),
        ).save()
        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.get("/api/v1/student/projects", headers={
            "Authorization": f"Bearer {token}"
        })
        data = resp.json

        assert resp.status_code == 200
        assert type(data['data']['modules']) == list
        assert len(data['data']['modules']) == 1
        assert type(data['data']['modules'][0]['projects']) == list
        assert len(data['data']['modules'][0]['projects']) == 1

def test_student_get_all_projects_no_modules(app, client, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = create_course
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=23),
        )
        cohort.save()
        cohort.refresh()
        data = {
            "email": "student@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_student1',
            "status": "active",
            "course_id": course['id'],
            "cohort_id": cohort.id,
        }
        student = Student(**data)
        student.save()
        student.refresh()

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.get("/api/v1/student/projects", headers={
            "Authorization": f"Bearer {token}"
        })
        data = resp.json

        assert resp.status_code == 200
        assert type(data['data']['modules']) == list
        assert len(data['data']['modules']) == 0