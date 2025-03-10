"""
Test cases for /api/v1/module/<module_id>/update PATCH endpoint
"""


def test_update_module_success(app, client, admin, auth, create_module):
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/module/{module['id']}/update",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "title": "Updated Module Title"
            }
        )

        assert response.status_code == 200
        assert response.json.get("data") is None
        from app.models.module import Module
        module = Module.search(id=module['id'])
        assert module.title == "Updated Module Title"

def test_update_module_user_role_not_admin(app, client, student, auth, create_module):
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        auth_r = auth.login(student.username, "test_password", "student")
        response = client.patch(f"/api/v1/module/{module['id']}/update",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "title": "Updated Module Title"
            }
        )

        assert response.status_code == 403
        assert response.json.get("data") is None
        from app.models.module import Module
        module = Module.search(id=module['id'])
        assert module.title == "Module 1"

def test_update_module_user_logged_out(app, client, create_module):
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        response = client.patch(f"/api/v1/module/{module['id']}/update",
            json={
                "title": "Updated Module Title"
            }
        )

        assert response.status_code == 401
        assert response.json.get("data") is None
        from app.models.module import Module
        module = Module.search(id=module['id'])
        assert module.title == "Module 1"

def test_update_module_invalid_module_id(app, client, admin, auth, create_module):
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/module/invalid-module-id/update",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "title": "Updated Module Title"
            }
        )

        assert response.status_code == 404
        assert response.json.get("data") is None
        from app.models.module import Module
        module = Module.search(id=module['id'])
        assert module.title == "Module 1"

def test_update_module_update_id_attribute(app, client, admin, auth, create_module):
    with app.test_request_context():
        app.preprocess_request()
        course, module = create_module
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/module/{module['id']}/update",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "id": 1,
                "title": "Updated Module Title"
            }
        )

        assert response.status_code == 200
        assert response.json.get("data") is None
        from app.models.module import Module
        module = Module.search(id=module['id'])
        assert module.title == "Updated Module Title"