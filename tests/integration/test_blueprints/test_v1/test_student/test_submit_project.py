"""
Test cases for /api/v1/student/project/<project_id>/submit POST endpoint
"""
from datetime import date, datetime, timedelta


def test_submit_project_success(app, client, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import CohortProject, StudentProject
        from app.models.cohort import Cohort
        course, models, project = create_project
        cohort = Cohort(
            course_id=course['id'],
            name="Cohort-1",
            status="in-progress",
            start_date=date.today() - timedelta(days=22),
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
        cohortProject_id = cohortProject.id
        student_id = student.id

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.post(f"/api/v1/student/project/{cohortProject.id}/submit",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "submission_file": "https://google.com/docs"
            }
        )

        assert resp.status_code == 200
        assert resp.json.get("data") is None
        studentProject = StudentProject.search(cohort_project_id=cohortProject_id, student_id=student_id)
        assert studentProject.status == "submitted"
        assert isinstance(studentProject.submitted_on, datetime)
        assert studentProject.submission_file == "https://google.com/docs"

def test_submit_project_user_logged_out(app, client, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import CohortProject, StudentProject
        from app.models.cohort import Cohort
        course, models, project = create_project
        cohort = Cohort(
            course_id=course['id'],
            name="Cohort-1",
            status="in-progress",
            start_date=date.today() - timedelta(days=22),
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
        cohortProject_id = cohortProject.id
        student_id = student.id

        resp = client.post(f"/api/v1/student/project/{cohortProject.id}/submit",
            json={
                "submission_file": "https://google.com/docs"
            }
        )

        assert resp.status_code == 401
        assert resp.json.get("data") is None
        assert StudentProject.search(cohort_project_id=cohortProject_id, student_id=student_id) is None

def test_submit_project_invalid_project_id(app, client, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import CohortProject, StudentProject
        from app.models.cohort import Cohort
        course, models, project = create_project
        cohort = Cohort(
            course_id=course['id'],
            name="Cohort-1",
            status="in-progress",
            start_date=date.today() - timedelta(days=22),
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
        cohortProject_id = cohortProject.id
        student_id = student.id

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        resp = client.post(f"/api/v1/student/project/invalid-project-id/submit",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "submission_file": "https://google.com/docs"
            }
        )

        assert resp.status_code == 400
        assert resp.json.get("data") is None
        assert StudentProject.search(cohort_project_id=cohortProject_id, student_id=student_id) is None
