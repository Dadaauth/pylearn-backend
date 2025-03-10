"""
Test cases for /api/v1/mentor/all GET endpoint
"""


def test_get_all_mentors_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dts = [
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor1@email.com",
                "username": "test_mentor1",
                "password": "test_password",
            },
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor2@email.com",
                "username": "test_mentor2",
                "password": "test_password",
            },
        ]
        for dt in dts:
            Mentor(**dt).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/mentor/all", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['mentors']) == list
        assert len(data['data']['mentors']) == 2
        assert data['data']['mentors'][0].get("password") is None
        assert data['data']['mentors'][1].get("password") is None
        assert data['data']['mentors'][0].get("id") is not None
        assert data['data']['mentors'][0].get("first_name") is not None
        assert data['data']['mentors'][0].get("last_name") is not None
        assert data['data']['mentors'][0].get("email") is not None
        assert data['data']['mentors'][0].get("status") is not None
        assert data['data']['mentors'][0].get("username") is not None

def test_get_all_mentors_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dts = [
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor1@email.com",
                "username": "test_mentor1",
                "password": "test_password",
            },
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor2@email.com",
                "username": "test_mentor2",
                "password": "test_password",
            },
        ]
        for dt in dts:
            Mentor(**dt).save()

        response = client.get("/api/v1/mentor/all")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_get_all_mentors_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dts = [
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor1@email.com",
                "username": "test_mentor1",
                "password": "test_password",
            },
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor2@email.com",
                "username": "test_mentor2",
                "password": "test_password",
            },
        ]
        for dt in dts:
            Mentor(**dt).save()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get("/api/v1/mentor/all", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None

def test_get_all_mentors_only_one_mentor(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dts = [
            {
                "first_name": "Test",
                "last_name": "Mentor",
                "email": "mentor1@email.com",
                "username": "test_mentor1",
                "password": "test_password",
            },
        ]
        for dt in dts:
            Mentor(**dt).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/mentor/all", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['mentors']) == list
        assert len(data['data']['mentors']) == 1
        assert data['data']['mentors'][0].get("password") is None
        assert data['data']['mentors'][0].get("id") is not None
        assert data['data']['mentors'][0].get("first_name") is not None
        assert data['data']['mentors'][0].get("last_name") is not None
        assert data['data']['mentors'][0].get("email") is not None
        assert data['data']['mentors'][0].get("status") is not None
        assert data['data']['mentors'][0].get("username") is not None

def test_get_all_mentors_no_mentors(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get("/api/v1/mentor/all", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['mentors']) == list
        assert len(data['data']['mentors']) == 0