"""
Test cases for /api/v1/project/<project_id>/assigned_submissions GET endpoint
"""
from datetime import date, timedelta


def test_get_assigned_submissions_success(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
        mentor_id = mentor.id
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=12)
        )
        cohort.refresh()
        cohort_id = cohort.id
        cohortProject = CohortProject(
            title="Project 1",
            module_id=module['id'],
            author_id=admin.id,
            course_id=course['id'],
            fa_start_date=date.today(),
            sa_start_date=date.today() + timedelta(days=4),
            end_date=date.today() + timedelta(days=6),
            cohort_id=cohort_id,
            project_pool_id=project['id'],
            status="released",
        )
        cohortProject.save()
        cohortProject.refresh()
        cohortProject_id = cohortProject.id
        student1 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student2@email.com",
            username="test_student2",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student1.save()
        student1.refresh()
        student1_id = student1.id
        student2 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student3@email.com",
            username="test_student3",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student2.save()
        student2.refresh()
        student2_id = student2.id
        studentProject1 = StudentProject(
            cohort_id=cohort_id,
            student_id=student1_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject1.save()
        studentProject1.refresh()
        studentProject1_id = studentProject1.id
        studentProject2 = StudentProject(
            cohort_id=cohort_id,
            student_id=student2_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject2.save()
        studentProject2.refresh()
        studentProject2_id = studentProject2.id

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/project/{cohortProject_id}/assigned_submissions", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['project']['id'] == cohortProject_id
        assert type(data['data']['data']) == list
        assert len(data['data']['data']) == 2
        assert data['data']['data'][0]['student']
        assert data['data']['data'][1]['student']
        assert data['data']['data'][0]['student'].get("password") is None
        assert data['data']['data'][1]['student'].get("password") is None
        assert data['data']['data'][0]['student_project']
        assert data['data']['data'][1]['student_project']

def test_get_assigned_submissions_no_assigned_projects(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
        mentor_id = mentor.id
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=12)
        )
        cohort.refresh()
        cohort_id = cohort.id
        cohortProject = CohortProject(
            title="Project 1",
            module_id=module['id'],
            author_id=admin.id,
            course_id=course['id'],
            fa_start_date=date.today(),
            sa_start_date=date.today() + timedelta(days=4),
            end_date=date.today() + timedelta(days=6),
            cohort_id=cohort_id,
            project_pool_id=project['id'],
            status="released",
        )
        cohortProject.save()
        cohortProject.refresh()
        cohortProject_id = cohortProject.id
        student1 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student2@email.com",
            username="test_student2",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student1.save()
        student1.refresh()
        student1_id = student1.id
        student2 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student3@email.com",
            username="test_student3",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student2.save()
        student2.refresh()
        student2_id = student2.id
        studentProject1 = StudentProject(
            cohort_id=cohort_id,
            student_id=student1_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject1.save()
        studentProject1.refresh()
        studentProject1_id = studentProject1.id
        studentProject2 = StudentProject(
            cohort_id=cohort_id,
            student_id=student2_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject2.save()
        studentProject2.refresh()
        studentProject2_id = studentProject2.id

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/project/{cohortProject_id}/assigned_submissions", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get('data') is None

def test_get_assigned_submissions_user_logged_out(app, client, admin, mentor, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
        mentor_id = mentor.id
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=12)
        )
        cohort.refresh()
        cohort_id = cohort.id
        cohortProject = CohortProject(
            title="Project 1",
            module_id=module['id'],
            author_id=admin.id,
            course_id=course['id'],
            fa_start_date=date.today(),
            sa_start_date=date.today() + timedelta(days=4),
            end_date=date.today() + timedelta(days=6),
            cohort_id=cohort_id,
            project_pool_id=project['id'],
            status="released",
        )
        cohortProject.save()
        cohortProject.refresh()
        cohortProject_id = cohortProject.id
        student1 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student2@email.com",
            username="test_student2",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student1.save()
        student1.refresh()
        student1_id = student1.id
        student2 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student3@email.com",
            username="test_student3",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student2.save()
        student2.refresh()
        student2_id = student2.id
        studentProject1 = StudentProject(
            cohort_id=cohort_id,
            student_id=student1_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject1.save()
        studentProject1.refresh()
        studentProject1_id = studentProject1.id
        studentProject2 = StudentProject(
            cohort_id=cohort_id,
            student_id=student2_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject2.save()
        studentProject2.refresh()
        studentProject2_id = studentProject2.id

        response = client.get(f"/api/v1/project/{cohortProject_id}/assigned_submissions")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_get_assigned_submissions_student_user_role(app, client, admin, mentor, student, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
        mentor_id = mentor.id
        cohort = Cohort(
            name="Cohort-1",
            status="in-progress",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=12)
        )
        cohort.refresh()
        cohort_id = cohort.id
        cohortProject = CohortProject(
            title="Project 1",
            module_id=module['id'],
            author_id=admin.id,
            course_id=course['id'],
            fa_start_date=date.today(),
            sa_start_date=date.today() + timedelta(days=4),
            end_date=date.today() + timedelta(days=6),
            cohort_id=cohort_id,
            project_pool_id=project['id'],
            status="released",
        )
        cohortProject.save()
        cohortProject.refresh()
        cohortProject_id = cohortProject.id
        student1 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student2@email.com",
            username="test_student2",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student1.save()
        student1.refresh()
        student1_id = student1.id
        student2 = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student3@email.com",
            username="test_student3",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student2.save()
        student2.refresh()
        student2_id = student2.id
        studentProject1 = StudentProject(
            cohort_id=cohort_id,
            student_id=student1_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject1.save()
        studentProject1.refresh()
        studentProject1_id = studentProject1.id
        studentProject2 = StudentProject(
            cohort_id=cohort_id,
            student_id=student2_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
            assigned_to=mentor_id,
        )
        studentProject2.save()
        studentProject2.refresh()
        studentProject2_id = studentProject2.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/project/{cohortProject_id}/assigned_submissions", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None