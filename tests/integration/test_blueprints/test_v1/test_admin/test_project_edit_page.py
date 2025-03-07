"""
Test cases for /api/v1/admin/project/<project_id>/edit endpoint
"""


def test_admin_project_edit_page_patch_success(app, client, admin, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, project = create_project

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/admin/project/{project["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" },
            json={
                "title": "Updated Project Title",
                "description": "Added a Description",
            }
        )
        data = response.json

        assert response.status_code == 200
        assert data.get("message") is not None
        pjt = AdminProject.search(id=project["id"])
        assert pjt is not None
        assert pjt.title == "Updated Project Title"
        assert pjt.description == "Added a Description"

def test_admin_project_edit_page_patch_invalid_project_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/admin/project/invalid-project-id/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" },
            json={
                "title": "Updated Project Title",
                "description": "Added a Description",
            }
        )
        data = response.json

        assert response.status_code == 404
        assert data.get("message") is not None
        assert data.get("data") is None

def test_admin_project_edit_page_patch_user_not_logged_in(app, client, create_project):
    with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        response = client.patch(f"/api/v1/admin/project/{project["id"]}/edit",
            json={
                "title": "Updated Project Title",
                "description": "Added a Description",
            }
        )
        data = response.json

        assert response.status_code == 401
        assert data.get(("data")) is None

def test_admin_project_edit_page_patch_user_role_not_admin(app, client, student, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.patch(f"/api/v1/admin/project/{project["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" },
            json={
                "title": "Updated Project Title",
                "description": "Added a Description",
            }
        )
        data = response.json

        assert response.status_code == 403
        assert data.get('data') is None

def test_admin_project_edit_page_get_success(app, admin, auth, client, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        from app.models.project import AdminProject
        course, module, projects = create_projects
        dt = {
            "title": "Test Project 3",
            "module_id": module["id"],
            "author_id": admin.id,
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        AdminProject(**dt).save()

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/project/{projects[0]["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" }
        )
        data = response.json
        
        
        # creating other records under a different course to ensure only
        # records for the course where the current project is assigned are
        # returned
        course_z = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        coursez_dict = course_z.to_dict()
        course_z.save()
        module_z = Module(title="Module 1", course_id=coursez_dict["id"])
        modulez_dict = module_z.to_dict()
        module_z.save()
        dt = {
            "title": "Test Project",
            "module_id": modulez_dict["id"],
            "author_id": admin.id,
            "course_id": coursez_dict["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project_z = AdminProject(**dt)
        project_z.refresh()
        projectz_dict = project_z.to_dict()
        project_z.save()

        assert response.status_code == 200
        assert data['data']['currentProject']["id"] == projects[0]["id"]
        assert data['data']['currentProject'].get("module")["id"] == module["id"]
        assert len(data['data']['projects']) == 2
        assert data['data']['projects'][0]["id"] != projects[0]["id"]
        assert len(data['data']['modules']) == 1
        assert data['data']['modules'][0]['id'] == module["id"]

def test_admin_project_edit_page_get_one_module_no_other_projects(app, admin, auth, client, create_project):
     with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/project/{project["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" }
        )
        data = response.json

        assert response.status_code == 200
        assert data['data']['currentProject']["id"] == project["id"]
        assert data['data']['currentProject'].get("module")["id"] == module["id"]
        assert data['data']['projects'] == []
        assert len(data['data']['modules']) == 1
        assert data['data']['modules'][0]['id'] == module["id"]

def test_admin_project_edit_page_get_only_one_other_project(app, admin, auth, client, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        course, module, projects = create_projects

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/project/{projects[0]["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" }
        )
        data = response.json
        
        
        # creating other records under a different course to ensure only
        # records for the course where the current project is assigned are
        # returned
        from app.models.course import Course
        from app.models.module import Module
        from app.models.project import AdminProject
        course_z = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        coursez_dict = course_z.to_dict()
        course_z.save()
        module_z = Module(title="Module 1", course_id=coursez_dict["id"])
        modulez_dict = module_z.to_dict()
        module_z.save()
        dt = {
            "title": "Test Project",
            "module_id": modulez_dict["id"],
            "author_id": admin.id,
            "course_id": coursez_dict["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project_z = AdminProject(**dt)
        project_z.refresh()
        projectz_dict = project_z.to_dict()
        project_z.save()

        assert response.status_code == 200
        assert data['data']['currentProject']["id"] == projects[0]["id"]
        assert data['data']['currentProject'].get("module")["id"] == module["id"]
        assert len(data['data']['projects']) == 1
        assert data['data']['projects'][0]["id"] != projects[0]["id"]
        assert len(data['data']['modules']) == 1
        assert data['data']['modules'][0]['id'] == module["id"]

def test_admin_project_edit_page_invalid_project_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/project/invalid-project-id/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" }
        )
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_admin_project_edit_page_get_not_logged_in_user(app, client, create_project):
     with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        response = client.get(f"/api/v1/admin/project/{project["id"]}/edit")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_admin_project_edit_page_get_user_role_not_admin(app, student, auth, client, create_project):
     with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/admin/project/{project["id"]}/edit",
            headers={ "Authorization": f"Bearer {auth_r.json["data"]["access_token"]}" }
        )
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
