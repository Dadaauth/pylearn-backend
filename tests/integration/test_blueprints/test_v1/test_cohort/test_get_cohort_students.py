"""
Test cases for /api/v1/cohort/<cohort_id>/students GET endpoint
"""
from datetime import date, timedelta


def test_get_cohort_students_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", course_id=course_id, status="in-progress", start_date=str(date.today() + timedelta(days=34)))
        cohort.save()
        cohort.refresh()
        cohort_id = cohort.id
        students = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "student@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student1",
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "student2@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student2",
            },
        ]
        for student in students:
            Student(**student).save()
        auth_r = auth.login(admin.username, 'test_password', "admin")
        response = client.get(f'/api/v1/cohort/{cohort_id}/students',
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"}
        )
        data = response.json
        assert response.status_code == 200
        assert len(data['data']['cohort']['students']) == 2
        assert data['data']['cohort']['course']['id'] == course_id
        assert data['data']['cohort']['students'][0].get('password') is None
        assert data['data']['cohort']['students'][1].get('password') is None

def test_get_cohort_students_only_one_student(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", course_id=course_id, status="in-progress", start_date=str(date.today() + timedelta(days=34)))
        cohort.save()
        cohort.refresh()
        cohort_id = cohort.id
        students = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "student@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student1",
            },
        ]
        for student in students:
            Student(**student).save()
        auth_r = auth.login(admin.username, 'test_password', "admin")
        response = client.get(f'/api/v1/cohort/{cohort_id}/students',
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"}
        )
        data = response.json
        assert response.status_code == 200
        assert type(data['data']['cohort']['students']) == list
        assert len(data['data']['cohort']['students']) == 1
        assert data['data']['cohort']['course']['id'] == course_id
        assert data['data']['cohort']['students'][0].get('password') is None

def test_get_cohort_students_no_students(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", course_id=course_id, status="in-progress", start_date=str(date.today() + timedelta(days=34)))
        cohort.save()
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(admin.username, 'test_password', "admin")
        response = client.get(f'/api/v1/cohort/{cohort_id}/students',
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"}
        )
        data = response.json
        assert response.status_code == 200
        assert type(data['data']['cohort']['students']) == list
        assert len(data['data']['cohort']['students']) == 0
        assert data['data']['cohort']['course']['id'] == course_id

def test_get_cohort_students_invalid_cohort_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", course_id=course_id, status="in-progress", start_date=str(date.today() + timedelta(days=34)))
        cohort.save()
        cohort.refresh()
        cohort_id = cohort.id
        students = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "student@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student1",
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "student2@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student2",
            },
        ]
        for student in students:
            Student(**student).save()
        auth_r = auth.login(admin.username, 'test_password', "admin")
        response = client.get(f'/api/v1/cohort/invalid_cohort_id/students',
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"}
        )
        data = response.json
        assert response.status_code == 404
        assert data.get("data") is None

def test_get_cohort_students_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.user import Student
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", course_id=course_id, status="in-progress", start_date=str(date.today() + timedelta(days=34)))
        cohort.save()
        cohort.refresh()
        cohort_id = cohort.id
        students = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "student@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student1",
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "student2@email.com",
                "cohort_id": cohort_id,
                "course_id": course_id,
                "password": "test_password",
                "username": "test_student2",
            },
        ]
        for student in students:
            Student(**student).save()
        response = client.get(f'/api/v1/cohort/{cohort_id}/students')
        data = response.json
        assert response.status_code == 401
        assert data.get("data") is None