"""
Test cases for /api/v1/project/<project_id> GET endpoint
"""


def test_get_single_project_success(app, client, mentor, auth, create_project):
    course, module, project = create_project
    auth_r = auth.login(mentor.username, "test_password", "mentor")
    response = client.get(f"/api/v1/project/{project['id']}", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 200
    assert data['data']['project']['id'] == project['id']
    assert data['data']['project']['author'] is not None
    assert data['data']['project']['module'] is not None

def test_get_single_project_invalid_project_id(app, client, mentor, auth, create_project):
    course, module, project = create_project
    auth_r = auth.login(mentor.username, "test_password", "mentor")
    response = client.get(f"/api/v1/project/invalid-project-id", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 404
    assert data.get("data") is None

def test_get_single_project_user_logged_out(app, client, create_project):
    course, module, project = create_project
    response = client.get(f"/api/v1/project/{project['id']}")
    data = response.json

    assert response.status_code == 401
    assert data.get("data") is None

def test_get_single_project_user_role_is_student(app, client, student, auth, create_project):
    course, module, project = create_project
    auth_r = auth.login(student.username, "test_password", "student")
    response = client.get(f"/api/v1/project/{project['id']}", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 403
    assert data.get("data") is None

def test_get_single_project_user_role_is_admin(app, client, admin, auth, create_project):
    course, module, project = create_project
    auth_r = auth.login(admin.username, "test_password", "admin")
    response = client.get(f"/api/v1/project/{project['id']}", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
    })
    data = response.json

    assert response.status_code == 200
    assert data['data']['project']['id'] == project['id']
    assert data['data']['project']['author'] is not None
    assert data['data']['project']['module'] is not None