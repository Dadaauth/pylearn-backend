"""
Test cases for /api/v1/cohort/create endpoint
"""
from datetime import date, timedelta


def test_create_cohort_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",
            status="published",
            communication_channel="https://discord.com/invite"
        )
        course_dict = course.to_dict()
        course.save()
        auth_r = auth.login(admin.username, 'test_password', "admin")

        response = client.post('/api/v1/cohort/create',
            headers={"Authorization": f"Bearer {auth_r.json["data"]["access_token"]}"},
            json={
                "name": "Cohort-1",
                "start_date": str(date.today() + timedelta(days=23)),
                "course_id": course_dict["id"],
            }
        )

        print(response.json)
        assert response.status_code == 201
        assert response.json.get("data") is None
        assert response.json.get("message") is not None
        cohort = Cohort.search(name="Cohort-1", start_date=date.today() + timedelta(days=23),
                course_id=course_dict["id"])
        assert cohort is not None
        assert cohort.status == "pending"
        assert cohort.start_date == date.today() + timedelta(days=23)

def test_create_cohort_missing_keys(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",
            status="published",
            communication_channel="https://discord.com/invite"
        )
        course_dict = course.to_dict()
        course.save()
        auth_r = auth.login(admin.username, 'test_password', "admin")

        response = client.post('/api/v1/cohort/create',
            headers={"Authorization": f"Bearer {auth_r.json["data"]["access_token"]}"},
            json={
                "name": "Cohort-1",
                "start_date": str(date.today() + timedelta(days=23)),
            }
        )

        assert response.status_code == 400
        assert response.json.get("data") is None
        assert response.json.get("message") is not None
        assert Cohort.search(name="Cohort-1", start_date=date.today() + timedelta(days=23),
                course_id=course_dict["id"]) is None

def test_create_cohort_not_logged_in(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",
            status="published",
            communication_channel="https://discord.com/invite"
        )
        course_dict = course.to_dict()
        course.save()

        response = client.post('/api/v1/cohort/create',
            json={
                "name": "Cohort-1",
                "start_date": str(date.today() + timedelta(days=23)),
                "course_id": course_dict["id"],
            }
        )

        assert response.status_code == 401
        assert response.json.get("data") is None
        assert Cohort.search(name="Cohort-1", start_date=date.today() + timedelta(days=23),
                course_id=course_dict["id"]) is None

def test_create_cohort_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",
            status="published",
            communication_channel="https://discord.com/invite"
        )
        course_dict = course.to_dict()
        course.save()
        auth_r = auth.login(student.username, 'test_password', "student")

        response = client.post('/api/v1/cohort/create',
            headers={"Authorization": f"Bearer {auth_r.json["data"]["access_token"]}"},
            json={
                "name": "Cohort-1",
                "start_date": str(date.today() + timedelta(days=23)),
                "course_id": course_dict["id"],
            }
        )

        assert response.status_code == 403
        assert response.json.get("data") is None
        assert response.json.get("message") is not None
        assert Cohort.search(name="Cohort-1", start_date=date.today() + timedelta(days=23),
                course_id=course_dict["id"]) is None