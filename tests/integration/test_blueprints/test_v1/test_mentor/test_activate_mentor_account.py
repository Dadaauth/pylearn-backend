"""
Test cases for /api/v1/mentor/account/activate POST endpoint
"""


def test_activate_mentor_account_success(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dt = {
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "email": "mentor1@email.com",
            "username": "test_mentor1",
            "status": "inactive",
        }
        mentor = Mentor(**dt)
        mentor.save()
        mentor.refresh()

        response = client.post("/api/v1/mentor/account/activate", json={
            "email": mentor.email,
            "username": "test_mentor1",
            "password": "test_password",
            "phone": "190-test-phone",
        })

        assert response.status_code == 200
        assert response.json.get("data") is None

def test_activate_mentor_account_account_already_activated(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dt = {
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "email": "mentor1@email.com",
            "username": "test_mentor1",
            "status": "active",
        }
        mentor = Mentor(**dt)
        mentor.save()
        mentor.refresh()

        response = client.post("/api/v1/mentor/account/activate", json={
            "email": mentor.email,
            "username": "test_mentor1",
            "password": "test_password",
            "phone": "190-test-phone",
        })

        assert response.status_code == 400
        assert response.json.get("data") is None
        assert response.json['message'] == "Account Activated Already!!"


def test_activate_mentor_account_required_field_absent(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import Mentor
        dt = {
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "email": "mentor1@email.com",
            "username": "test_mentor1",
            "status": "inactive",
        }
        mentor = Mentor(**dt)
        mentor.save()
        mentor.refresh()

        response1 = client.post("/api/v1/mentor/account/activate", json={
            "email": mentor.email,
            "username": "test_mentor1",
            "password": "test_password",
        })
        response2 = client.post("/api/v1/mentor/account/activate", json={
            "email": mentor.email,
            "username": "test_mentor1",
            "phone": "190-test-phone",
        })
        response3 = client.post("/api/v1/mentor/account/activate", json={
            "email": mentor.email,
            "password": "test_password",
            "phone": "190-test-phone",
        })
        response4 = client.post("/api/v1/mentor/account/activate", json={
            "username": "test_mentor1",
            "password": "test_password",
            "phone": "190-test-phone",
        })

        assert response1.status_code == 400
        assert response2.status_code == 400
        assert response3.status_code == 400
        assert response4.status_code == 400