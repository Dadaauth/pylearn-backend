"""
Test cases for /api/v1/module/create POST endpoint
"""


def test_create_module_success(app, client, admin, auth, create_course):
    course = create_course
    auth_r = auth.login(admin.username, "test_password", "admin")
    response = client.post("/api/v1/module/create",
        headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
        json={
            "title": "Module 1",
            "course_id": course['id'],
        }
    )

    with app.test_request_context():
        app.preprocess_request()
        from app.models.module import Module
        assert response.status_code == 201
        assert response.json.get("data") is None
        assert response.json.get("message") is not None
        modules = Module.all()
        assert type(modules) == list
        assert len(modules) == 1

def test_create_module_user_logged_out(app, client, create_course):
    course = create_course
    response = client.post("/api/v1/module/create",
        json={
            "title": "Module 1",
            "course_id": course['id'],
        }
    )

    assert response.status_code == 401
    assert response.json.get("data") is None

def test_create_module_user_role_not_admin(app, client, student, auth, create_course):
    course = create_course
    auth_r = auth.login(student.username, "test_password", "student")
    response = client.post("/api/v1/module/create",
        headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
        json={
            "title": "Module 1",
            "course_id": course['id'],
        }
    )

    assert response.status_code == 403
    assert response.json.get("data") is None
