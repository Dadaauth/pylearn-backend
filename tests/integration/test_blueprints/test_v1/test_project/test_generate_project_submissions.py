"""
Test cases for /api/v1/project/<project_id>/submissions/generate GET endpoint
"""
from datetime import date, timedelta


def test_project_submission_generation_success(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
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
        student = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student1@email.com",
            username="test_student1",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student.save()
        student.refresh()
        student_id = student.id
        studentProject = StudentProject(
            cohort_id=cohort_id,
            student_id=student_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject.save()
        studentProject.refresh()
        studentProject_id = studentProject.id

        mentor_id = mentor.id
        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/project/{cohortProject_id}/submissions/generate", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })

        assert response.status_code == 200
        assert response.json.get("data") is None
        updated_studentProject = StudentProject.search(id=studentProject_id)
        assert updated_studentProject.assigned_to == mentor_id


def test_project_submission_generation_student_user_role(app, client, admin, student, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
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
        student = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student2@email.com",
            username="test_student2",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student.save()
        student.refresh()
        student_id = student.id
        studentProject = StudentProject(
            cohort_id=cohort_id,
            student_id=student_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject.save()
        studentProject.refresh()
        studentProject_id = studentProject.id

        student_id = student.id
        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/project/{cohortProject_id}/submissions/generate", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })

        assert response.status_code == 403
        assert response.json.get("data") is None
        updated_studentProject = StudentProject.search(id=studentProject_id)
        assert updated_studentProject.assigned_to is None


def test_project_submission_generation_user_logged_out(app, client, admin, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
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
        student = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student1@email.com",
            username="test_student1",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student.save()
        student.refresh()
        student_id = student.id
        studentProject = StudentProject(
            cohort_id=cohort_id,
            student_id=student_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject.save()
        studentProject.refresh()
        studentProject_id = studentProject.id

        response = client.get(f"/api/v1/project/{cohortProject_id}/submissions/generate")

        assert response.status_code == 401
        assert response.json.get("data") is None
        updated_studentProject = StudentProject.search(id=studentProject_id)
        assert updated_studentProject.assigned_to is None

def test_project_submission_generation_no_submitted_projects(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
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
        student = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student1@email.com",
            username="test_student1",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student.save()
        student.refresh()

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/project/{cohortProject_id}/submissions/generate", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })

        assert response.status_code == 404
        assert response.json.get("data") is None


def test_project_submission_generation_invalid_project_id(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Student
        from app.models.project import StudentProject, CohortProject
        from app.models.cohort import Cohort
        course, module, project = create_project
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
        student = Student(
            first_name="Test",
            last_name="Last",
            password="test_password",
            email="student1@email.com",
            username="test_student1",
            course_id=course['id'],
            cohort_id=cohort_id
        )
        student.save()
        student.refresh()
        student_id = student.id
        studentProject = StudentProject(
            cohort_id=cohort_id,
            student_id=student_id,
            cohort_project_id=cohortProject_id,
            submission_file="https://google.com",
            submitted_on=date.today(),
            status="submitted",
        )
        studentProject.save()
        studentProject.refresh()
        studentProject_id = studentProject.id

        mentor_id = mentor.id
        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/project/invalid-project-id/submissions/generate", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })

        assert response.status_code == 404
        assert response.json.get("data") is None
        updated_studentProject = StudentProject.search(id=studentProject_id)
        assert updated_studentProject.assigned_to is None