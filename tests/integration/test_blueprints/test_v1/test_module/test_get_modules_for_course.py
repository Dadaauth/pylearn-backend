"""
Test cases for /api/v1/module/<course_id>/all GET endpoint
"""


def test_fetch_modules_success(app, client, student, auth, create_module):
    course, module = create_module

    auth_r = auth.login(student.username, "test_password", "student")
    response = client.get(f"/api/v1/module/{course['id']}/all", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 200
    assert type(data['data']['modules']) == list
    assert len(data['data']['modules']) == 1
    assert data['data']['modules'][0]['id'] == module['id']

def test_fetch_modules_user_logged_out(app, client, create_module):
    course, module = create_module

    response = client.get(f"/api/v1/module/{course['id']}/all")
    data = response.json

    assert response.status_code == 401
    assert data.get("data") is None

def test_fetch_modules_no_module(app, client, student, auth, create_course):
    course = create_course

    auth_r = auth.login(student.username, "test_password", "student")
    response = client.get(f"/api/v1/module/{course['id']}/all", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 404
    assert data.get("data") is None
    assert data['message'] is not None