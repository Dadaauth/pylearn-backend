"""
Test cases for /api/v1/cohort/<cohort_id>/add-students POST endpoint
"""
from datetime import date, timedelta


def test_add_students_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published",\
            communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress", course_id=course_id,\
            start_date=str(date.today() + timedelta(days=14)))
        cohort.refresh()
        cohort_id = cohort.id
        student = Student(
            first_name="Test",
            last_name="Last",
            email="student@email.com",
            username="test_student1",
            password="test_password",
            status="inactive",
            course_id=course_id,
        )
        student.save()
        student.refresh()
        student_id = student.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.post(f"/api/v1/cohort/{cohort_id}/add-students",
            headers={
                "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
            },
            content_type='multipart/form-data',
            data={'student_ids': [student_id]},
        )
        data = response.json

        assert response.status_code == 200
        assert data.get("data") is None
        student = Student.search(id=student_id)
        assert student.cohort_id == cohort_id
        assert student.status == "active"

def test_add_students_invalid_cohort_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published",\
            communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress", course_id=course_id,\
            start_date=str(date.today() + timedelta(days=14)))
        cohort.refresh()
        cohort_id = cohort.id
        student = Student(
            first_name="Test",
            last_name="Last",
            email="student@email.com",
            username="test_student1",
            password="test_password",
            status="inactive",
            course_id=course_id,
        )
        student.save()
        student.refresh()
        student_id = student.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.post(f"/api/v1/cohort/invalid-cohort-id/add-students",
            headers={
                "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
            },
            content_type='multipart/form-data',
            data={'student_ids': [student_id]},
        )
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None
        student = Student.search(id=student_id)
        assert student.cohort_id is None
        assert student.status == "inactive"

def test_add_students_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published",\
            communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress", course_id=course_id,\
            start_date=str(date.today() + timedelta(days=14)))
        cohort.refresh()
        cohort_id = cohort.id
        student = Student(
            first_name="Test",
            last_name="Last",
            email="student@email.com",
            username="test_student1",
            password="test_password",
            status="inactive",
            course_id=course_id,
        )
        student.save()
        student.refresh()
        student_id = student.id

        response = client.post(f"/api/v1/cohort/{cohort_id}/add-students",
            content_type='multipart/form-data',
            data={'student_ids': [student_id]},
        )
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None
        student = Student.search(id=student_id)
        assert student.cohort_id is None
        assert student.status == "inactive"

def test_add_students_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published",\
            communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress", course_id=course_id,\
            start_date=str(date.today() + timedelta(days=14)))
        cohort.refresh()
        cohort_id = cohort.id
        student_obj = Student(
            first_name="Test",
            last_name="Last",
            email="student233@email.com",
            username="test_student123",
            password="test_password",
            status="inactive",
            course_id=course_id,
        )
        student_obj.save()
        student_obj.refresh()
        student_id = student_obj.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.post(f"/api/v1/cohort/{cohort_id}/add-students",
            headers={
                "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
            },
            content_type='multipart/form-data',
            data={'student_ids': [student_id]},
        )
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
        student = Student.search(id=student_id)
        assert student.cohort_id is None
        assert student.status == "inactive"
