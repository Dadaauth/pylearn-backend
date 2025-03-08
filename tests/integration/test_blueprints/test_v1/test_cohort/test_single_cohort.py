"""
Test cases for /api/v1/cohort/<cohort_id> GET, PATCH, and DELETE endpoint
"""
from datetime import date, timedelta


def test_delete_single_cohort_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.delete(f"/api/v1/cohort/{cohort_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data.get('data') is None
        assert data.get('message') is not None
        assert Cohort.search(id=cohort_id) is None

def test_delete_single_cohort_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        response = client.delete(f"/api/v1/cohort/{cohort_id}")
        data = response.json

        assert response.status_code == 401
        assert data.get('data') is None
        assert Cohort.search(id=cohort_id) is not None

def test_delete_single_cohort_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.delete(f"/api/v1/cohort/{cohort_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get('data') is None
        assert Cohort.search(id=cohort_id) is not None

def test_delete_single_cohort_invalid_cohort_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.delete(f"/api/v1/cohort/invalid-cohort-id", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get('data') is None

def test_update_single_cohort_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/cohort/{cohort_id}", json={
            "name": "Cohort-2",
            "status": "completed"
        }, headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data.get('data') is None
        assert data.get('message') is not None
        assert Cohort.search(id=cohort_id).status == "completed"
        assert Cohort.search(id=cohort_id).name == "Cohort-2"

def test_update_single_cohort_update_cohort_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/cohort/{cohort_id}", json={
            "id": "new-cohort-id",
            "name": "Cohort-2",
            "status": "completed"
        }, headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data.get('data') is None
        assert data.get('message') is not None
        cohort = Cohort.search(id=cohort_id)
        assert cohort.status == "completed"
        assert cohort.name == "Cohort-2"
        assert cohort.id == cohort_id # The id should not be updated

def test_update_single_cohort_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        response = client.patch(f"/api/v1/cohort/{cohort_id}", json={
            "name": "Cohort-2",
            "status": "completed"
        })
        data = response.json

        assert response.status_code == 401
        assert data.get('data') is None
        assert Cohort.search(id=cohort_id).status == "in-progress"
        assert Cohort.search(id=cohort_id).name == "Cohort-1"

def test_update_single_cohort_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.patch(f"/api/v1/cohort/{cohort_id}", json={
            "name": "Cohort-2",
            "status": "completed"
        }, headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get('data') is None
        assert Cohort.search(id=cohort_id).status == "in-progress"
        assert Cohort.search(id=cohort_id).name == "Cohort-1"

def test_update_single_cohort_invalid_cohort_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch("/api/v1/cohort/invalid-cohort_id", json={
            "name": "Cohort-2",
            "status": "completed"
        }, headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get('data') is None

def test_get_single_cohort_page_success(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/cohort/{cohort_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['cohort']['id'] == cohort_id
        assert data['data']['cohort']['course']['id'] == course_id

def test_get_single_cohort_page_wrong_cohort_id(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/cohort/wrong-cohort_id", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_get_single_cohort_page_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course = Course(title="Software Engineering",\
            status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort = Cohort(name="Cohort-1", status="in-progress",\
            course_id=course.id, start_date=str(date.today() + timedelta(days=12)))
        cohort.refresh()
        cohort_id = cohort.id

        response = client.get(f"/api/v1/cohort/{cohort_id}")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None