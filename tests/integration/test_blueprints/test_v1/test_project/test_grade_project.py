"""
Test cases for /api/v1/project/grade PATCH endpoint
"""
from datetime import date, datetime, timedelta


def test_grade_project_success(app, client, admin, mentor, auth, create_project):
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
        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json['message'] == "Grading successful"
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "graded"
        assert isinstance(studentProject.graded_on, datetime)
        assert studentProject.graded_by == mentor_id
        assert studentProject.feedback == "Good job"
        assert studentProject.grade == 100

def test_grade_project_submission_during_second_attempt(app, client, admin, mentor, auth, create_project):
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
            fa_start_date=date.today() - timedelta(days=3),
            sa_start_date=date.today(),
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
        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json['message'] == "Grading successful"
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "graded"
        assert isinstance(studentProject.graded_on, datetime)
        assert studentProject.graded_by == mentor_id
        assert studentProject.feedback == "Good job"
        assert studentProject.grade == 65

def test_grade_project_submission_when_project_has_ended(app, client, admin, mentor, auth, create_project):
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
            fa_start_date=date.today() - timedelta(days=6),
            sa_start_date=date.today() - timedelta(days=3),
            end_date=date.today(),
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
        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json['message'] == "Grading successful"
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "graded"
        assert isinstance(studentProject.graded_on, datetime)
        assert studentProject.graded_by == mentor_id
        assert studentProject.feedback == "Good job"
        assert studentProject.grade == 50

def test_grade_project_invalid_student_project_id(app, client, admin, mentor, auth, create_project):
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
        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": "invalid-id",
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "submitted"
        assert studentProject.graded_on is None
        assert studentProject.graded_by is None
        assert studentProject.feedback is None
        assert studentProject.grade is None

def test_grade_project_required_fields_not_sent(app, client, admin, mentor, auth, create_project):
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
        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 400
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "submitted"
        assert studentProject.graded_on is None
        assert studentProject.graded_by is None
        assert studentProject.feedback is None
        assert studentProject.grade is None

        response = client.patch(
            "/api/v1/project/grade",
            json={
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 400
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "submitted"
        assert studentProject.graded_on is None
        assert studentProject.graded_by is None
        assert studentProject.feedback is None
        assert studentProject.grade is None

def test_grade_project_student_user_role(app, client, admin, mentor, student, auth, create_project):
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
        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "grade": 100,
                "feedback": "Good job"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "submitted"
        assert studentProject.graded_on is None
        assert studentProject.graded_by is None
        assert studentProject.feedback is None
        assert studentProject.grade is None

def test_grade_project_user_logged_out(app, client, admin, mentor, create_project):
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
        response = client.patch(
            "/api/v1/project/grade",
            json={
                "student_project_id": studentProject_id,
                "grade": 100,
                "feedback": "Good job"
            },
        )

        assert response.status_code == 401
        studentProject = StudentProject.search(id=studentProject_id)
        assert studentProject.status == "submitted"
        assert studentProject.graded_on is None
        assert studentProject.graded_by is None
        assert studentProject.feedback is None
        assert studentProject.grade is None
