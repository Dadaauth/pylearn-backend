"""
Test cases for /api/v1/cohort/all endpoint
"""
from datetime import date, timedelta


def test_get_all_cohorts_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course_id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course_id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        cohorts = []
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            cohorts.append(cohort.to_dict())

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/cohort/all", headers={
            "Authorization": f"Bearer {auth_r.json["data"]['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data['data']['cohorts']) == 2
        assert data['data']['cohorts'][0]['course']['id'] == course_id

def test_get_all_cohorts_user_not_logged_in(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course.id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course.id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        cohorts = []
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            cohorts.append(cohort.to_dict())

        response = client.get("/api/v1/cohort/all")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_get_all_cohorts_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course.id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course.id,
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        cohorts = []
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            cohorts.append(cohort.to_dict())

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get("/api/v1/cohort/all", headers={
            "Authorization": f"Bearer {auth_r.json["data"]['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None

def test_get_all_cohorts_only_one_cohort(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dt = {
            "name": "Cohort-1",
            "course_id": course_id,
            "status": "in-progress",
            "start_date": str(date.today() + timedelta(days=34)),
        }
        cohort = Cohort(**dt)
        cohort.refresh()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/cohort/all", headers={
            "Authorization": f"Bearer {auth_r.json["data"]['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data['data']['cohorts']) == 1
        assert type(data['data']['cohorts']) == list
        assert data['data']['cohorts'][0]['course']['id'] == course_id

def test_get_all_cohorts_no_cohorts(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/cohort/all", headers={
            "Authorization": f"Bearer {auth_r.json["data"]['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None
