"""
Test cases for /api/v1/admin/<course_id>/projects endpoint
"""

def test_adminprojects_page_success(admin, client, auth, create_course_and_modules):
    course, modules = create_course_and_modules
    response = auth.login("test_admin1", "test_password", "admin")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 200
    assert data.get("data") is not None
    assert "modules" in data.get("data")
    assert len(data.get("data").get("modules")) == len(modules)
    assert data.get("data").get("modules")[0].get("projects") is not None
    assert data.get("data").get("modules")[0].get("projects") == []
    assert data.get("data").get("modules")[1].get("projects") is not None
    assert data.get("data").get("modules")[1].get("projects") == []

def test_adminprojects_page_one_module_success(admin, client, auth, create_module):
    course, module = create_module
    response = auth.login("test_admin1", "test_password", "admin")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 200
    assert data.get("data") is not None
    assert "modules" in data.get("data")
    assert len(data.get("data").get("modules")) == 1
    assert data.get("data").get("modules")[0].get("projects") is not None
    assert data.get("data").get("modules")[0].get("projects") == []

def test_adminprojects_page_has_a_projects(admin, client, auth, create_project):
    course, module, project = create_project
    response = auth.login("test_admin1", "test_password", "admin")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 200
    assert data.get("data") is not None
    assert "modules" in data.get("data")
    assert len(data.get("data").get("modules")) == 1
    assert len(data.get("data").get("modules")[0].get("projects")) == 1

def test_adminprojects_page_has_multiple_projects(admin, client, auth, create_projects):
    course, module, projects = create_projects
    response = auth.login("test_admin1", "test_password", "admin")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 200
    assert data.get("data") is not None
    assert "modules" in data.get("data")
    assert len(data.get("data").get("modules")) == 1
    assert len(data.get("data").get("modules")[0].get("projects")) == 2

def test_adminprojects_page_no_modules(admin, client, auth, create_course):
    course = create_course
    response = auth.login("test_admin1", "test_password", "admin")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 200
    assert data["data"]["modules"] == []
    assert data["statusCode"] == 200

def test_adminprojects_page_unauthorized(client, create_course):
    course = create_course
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]))
    data = response.json

    assert response.status_code == 401
    assert data.get("data") is None

def test_adminprojects_not_admin_role(client, create_course, student, auth):
    course = create_course
    response = auth.login("test_student1", "test_password", "student")
    response = client.get('/api/v1/admin/{}/projects'.format(course["id"]), headers={
        "Authorization": f"Bearer {response.json.get('data').get('access_token')}"
    })
    data = response.json

    assert response.status_code == 403
    assert data.get("data") is None
