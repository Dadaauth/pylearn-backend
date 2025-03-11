"""
Test cases for /api/v1/project/edit/<project_id> PATCH endpoint
"""


def test_project_update_success(app, client, create_project, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, project = create_project
        project_id = project["id"]

        token = auth.login(admin.username, "test_password", "admin").json['data']['access_token']
        response = client.patch(f"/api/v1/project/edit/{project_id}", 
            headers={"Authorization": f"Bearer {token}"},
            json={
                "id": "1",
                "title": "Updated Project Title",
            }
        )

        assert response.status_code == 200
        assert response.json.get("data") is None
        project = AdminProject.search(id=project_id)
        assert project.title == "Updated Project Title"
        assert project.status == "published"

def test_project_update_user_role_not_admin(app, client, create_project, mentor, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, project = create_project
        project_id = project["id"]

        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.patch(f"/api/v1/project/edit/{project_id}", 
            headers={"Authorization": f"Bearer {token}"},
            json={
                "id": "1",
                "title": "Updated Project Title",
            }
        )

        assert response.status_code == 403
        assert response.json.get("data") is None
        project = AdminProject.search(id=project_id)
        assert project.title == "Test Project"
        assert project.status == "published"

def test_project_update_user_logged_out(app, client, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, project = create_project
        project_id = project["id"]

        response = client.patch(f"/api/v1/project/edit/{project_id}", 
            json={
                "id": "1",
                "title": "Updated Project Title",
            }
        )

        assert response.status_code == 401
        assert response.json.get("data") is None
        project = AdminProject.search(id=project_id)
        assert project.title == "Test Project"
        assert project.status == "published"

def test_project_update_invalid_project_id(app, client, create_project, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, project = create_project
        project_id = project["id"]

        token = auth.login(admin.username, "test_password", "admin").json['data']['access_token']
        response = client.patch(f"/api/v1/project/edit/invalid-project_id", 
            headers={"Authorization": f"Bearer {token}"},
            json={
                "id": "1",
                "title": "Updated Project Title",
            }
        )

        assert response.status_code == 400
        assert response.json.get("data") is None
        project = AdminProject.search(id=project_id)
        assert project.title == "Test Project"
        assert project.status == "published"