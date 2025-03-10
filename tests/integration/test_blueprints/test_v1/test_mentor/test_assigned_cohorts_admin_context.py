"""
Test cases for /api/v1/mentor/<mentor_id>/assigned_cohorts GET endpoint
"""
from datetime import date, timedelta


def test_get_assigned_cohorts_success(app, client, mentor, admin, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        course = create_course
        mentor_id = mentor.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort.id).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/mentor/{mentor_id}/assigned_cohorts", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['cohorts']) == list
        assert len(data['data']['cohorts']) == 2
        assert data['data']['cohorts'][0]['course']['id'] == course['id']

def test_get_assigned_cohorts_only_one_cohort(app, client, mentor, admin, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        course = create_course
        mentor_id = mentor.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort.id).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/mentor/{mentor_id}/assigned_cohorts", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['cohorts']) == list
        assert len(data['data']['cohorts']) == 1
        assert data['data']['cohorts'][0]['course']['id'] == course['id']

def test_get_assigned_cohorts_no_cohorts(app, client, mentor, admin, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        mentor_id = mentor.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/mentor/{mentor_id}/assigned_cohorts", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_get_assigned_cohorts_invalid_mentor_id(app, client, mentor, admin, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        course = create_course
        mentor_id = mentor.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort.id).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/mentor/invalid-mentor-id/assigned_cohorts", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_get_assigned_cohorts_user_logged_out(app, client, mentor, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        course = create_course
        mentor_id = mentor.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort.id).save()

        response = client.get(f"/api/v1/mentor/{mentor_id}/assigned_cohorts")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_get_assigned_cohorts_user_role_not_admin(app, client, mentor, student, auth, create_course):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        from app.models.cohort import Cohort
        course = create_course
        mentor_id = mentor.id
        dts = [
            {
                "name": "Cohort-1",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
            {
                "name": "Cohort-2",
                "course_id": course['id'],
                "status": "in-progress",
                "start_date": str(date.today() + timedelta(days=34)),
            },
        ]
        for dt in dts:
            cohort = Cohort(**dt)
            cohort.refresh()
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort.id).save()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/mentor/{mentor_id}/assigned_cohorts", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None