"""
Test cases for /api/v1/auth/register endpoint
"""
import os
from tests.utils import create_user


def test_register_get_request(client):
    """
    GIVEN: A Flask test client
    WHEN: A GET request is made to the /api/v1/auth/register endpoint
    THEN: The response status code should be 405 (Method Not Allowed)
    """
    response = client.get("/api/v1/auth/register")
    assert response.status_code == 405

def test_register_admin_success(app, client):
    """
    Test the successful registration of an admin user.

    GIVEN:  A Flask application instance and a test client.
    WHEN:   A POST request is made to the /api/v1/auth/register endpoint with valid admin registration data.
    THEN:   The response status code should be 201.
            The response data should contain the registered user's details, excluding the password.
            The registered user's details should match the provided input data.
            The user should be successfully created in the database with the role of admin.
    """
    from app.models.user import Admin
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    data = response.json
    assert response.status_code == 201
    assert data.get("data").get("user")
    assert data.get("data").get("user").get("first_name") == "Test"
    assert data.get("data").get("user").get("last_name") == "Last"
    assert data.get("data").get("user").get("password") is None
    assert data.get("data").get("user").get("email") == "admin1@email.com"
    assert data.get("statusCode") == 201
    assert data.get("message")

    with app.test_request_context():
        app.preprocess_request()
        user_id = data.get("data").get("user").get("id")
        assert Admin.search(id=user_id).id == user_id

def test_register_mentor_success(app, client, auth):
    """
    Test the successful registration of a mentor.
    This test performs the following steps:
    1. Creates an admin user.
    2. Logs in as the admin user to obtain an access token.
    3. Uses the access token to register a new mentor.
    4. Asserts that the registration was successful by checking the response status code and data.
    5. Verifies that the mentor's details are correct and that the password is not returned in the response.
    6. Checks that the mentor exists in the database.
    Args:
        app: The Flask application instance.
        client: The test client for making requests to the application.
        auth: The authentication utility for logging in users.
    
    """
    from app.models.user import Mentor
    response = create_user(client, {
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response = auth.login("test_admin1", "test_password", "admin")
    access_token = response.json["data"].get("access_token")

    response = client.post("/api/v1/auth/register", json={
        "email": "mentor@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    data = response.json
    assert response.status_code == 201
    assert data.get("data").get("user")
    assert data.get("data").get("user").get("first_name") == "Test"
    assert data.get("data").get("user").get("last_name") == "Last"
    assert data.get("data").get("user").get("password") is None
    assert data.get("data").get("user").get("email") == "mentor@email.com"
    assert data.get("statusCode")
    assert data.get("message")

    with app.test_request_context():
        app.preprocess_request()
        user_id = data.get("data").get("user").get("id")
        assert Mentor.search(id=user_id).id == user_id

def test_register_admin_incomplete_data(app, client):
    """
    Test the successful registration of an admin user.

    GIVEN:  A Flask application instance and a test client.
    WHEN:   A POST request is made to the /api/v1/auth/register endpoint with valid admin registration data.
    THEN:   The response status code should be 201.
            The response data should contain the registered user's details, excluding the password.
            The registered user's details should match the provided input data.
            The user should be successfully created in the database with the role of admin.
    """
    response1 = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    response2 = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "username": "test_admin1",
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    response3 = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "password": "test_password",
        "username": "test_admin1",
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    response4 = client.post("/api/v1/auth/register", json={
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": "test_admin1",
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    response5 = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "last_name": "Last",
        "password": "test_password",
        "username": "test_admin1",
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    assert response1.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400
    assert response4.status_code == 400
    assert response5.status_code == 400

def test_register_mentor_incomplete_data(app, client, auth):
    """
    Test the successful registration of a mentor.
    This test performs the following steps:
    1. Creates an admin user.
    2. Logs in as the admin user to obtain an access token.
    3. Uses the access token to register a new mentor.
    4. Asserts that the registration was successful by checking the response status code and data.
    5. Verifies that the mentor's details are correct and that the password is not returned in the response.
    6. Checks that the mentor exists in the database.
    Args:
        app: The Flask application instance.
        client: The test client for making requests to the application.
        auth: The authentication utility for logging in users.
    
    """
    response = create_user(client, {
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response = auth.login("test_admin1", "test_password", "admin")
    access_token = response.json["data"].get("access_token")

    response1 = client.post("/api/v1/auth/register", json={
        "email": "mentor@email.com",
        "first_name": "Test",
        "username": "test_mentor",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    response2 = client.post("/api/v1/auth/register", json={
        "email": "mentor@email.com",
        "last_name": "Last",
        "username": "test_mentor",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    response3 = client.post("/api/v1/auth/register", json={
        "first_name": "Test",
        "last_name": "Last",
        "username": "test_mentor",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response1.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400

def test_register_mentor_not_admin_client(app, client, auth):
    from app.models.user import Mentor
    with app.test_request_context():
        app.preprocess_request()
        data = {
            "email": "mentor@email.com",
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "username": 'test_mentor1',
        }
        Mentor(**data).save()

    response = auth.login("test_mentor1", "test_password", "mentor")
    access_token = response.json["data"].get("access_token")

    response = client.post("/api/v1/auth/register", json={
        "email": "mentor1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 401

def test_register_mentor_not_logged_in(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "mentor1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "role": "mentor",
    })

    assert response.status_code == 401

def test_register_admin_no_reg_code(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
    })
    assert response.status_code == 401

def test_register_admin_wrong_reg_code(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": "incorrect admin registration code",
    })
    assert response.status_code == 401

def test_register_admin_user_exists(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    assert response.status_code == 400

def test_register_mentor_user_exists(client, auth):
    response = create_user(client, {
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "admin",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })

    response = auth.login("test_admin1", "test_password", "admin")
    access_token = response.json["data"].get("access_token")

    response = client.post("/api/v1/auth/register", json={
        "email": "mentor@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    response = client.post("/api/v1/auth/register", json={
        "email": "mentor@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "role": "mentor",
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 400

def test_register_wrong_role(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "wrong",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    assert response.status_code == 400

def test_register_student_role(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "role": "student",
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    assert response.status_code == 400

def test_register_no_role(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "admin1@email.com",
        "first_name": "Test",
        "last_name": "Last",
        "password": "test_password",
        "username": 'test_admin1',
        "admin_reg_code": os.getenv("ADMIN_REGISTRATION_PASSCODE"),
    })
    assert response.status_code == 400