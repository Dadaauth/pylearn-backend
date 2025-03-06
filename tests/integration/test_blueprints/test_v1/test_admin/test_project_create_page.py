"""
Test cases for /api/v1/admin/<course_id>/project/new endpoint
"""

def test_project_create_page_post_success(app, client, admin, auth, create_module):
    course, module = create_module

    auth_r = auth.login(admin.username, "test_password", "admin")
    response = client.post(f"/api/v1/admin/{course["id"]}/project/new",
        headers={"Authorization": f"Bearer {auth_r.json.get("data")["access_token"]}"},
        json={
            "title": "Test Project",
            "module_id": module["id"],
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
    )
    data = response.json

    assert response.status_code == 201
    assert data.get("data") is None
    assert data.get("message")

    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        assert AdminProject.search(
            title="Test Project", module_id=module["id"],
            course_id=course["id"], fa_duration=2,
            sa_duration=1,
            release_range=3,
            status="published"
        ) is not None

def test_project_create_page_post_user_not_logged_in(app, client, create_module):
    course, module = create_module

    response = client.post(f"/api/v1/admin/{course["id"]}/project/new",
        json={
            "title": "Test Project",
            "module_id": module["id"],
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
    )
    data = response.json

    assert response.status_code == 401
    assert data.get("data") is None

    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        assert AdminProject.search(
            title="Test Project", module_id=module["id"],
            course_id=course["id"], fa_duration=2,
            sa_duration=1,
            release_range=3,
            status="published"
        ) is None

def test_project_create_page_post_user_role_not_admin(app, client, student, auth, create_module):
    course, module = create_module

    auth_r = auth.login(student.username, "test_password", "student")
    response = client.post(f"/api/v1/admin/{course["id"]}/project/new",
        headers={"Authorization": f"Bearer {auth_r.json.get("data")["access_token"]}"},
        json={
            "title": "Test Project",
            "module_id": module["id"],
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
    )
    data = response.json

    assert response.status_code == 403
    assert data.get("data") is None

    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        assert AdminProject.search(
            title="Test Project", module_id=module["id"],
            course_id=course["id"], fa_duration=2,
            sa_duration=1,
            release_range=3,
            status="published"
        ) is None

def test_project_create_page_get_success(app, client, admin, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.module import Module
        from app.models.course import Course
        from app.models.project import AdminProject
        course, module, projects = create_projects
        Module(title="Test Module", course_id=course["id"]).save()

        # create another set of course, module and project to confirm that only
        # details for the specified course are returned
        course_z = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        coursez_dict = course_z.to_dict()
        course_z.save()
        module_z = Module(title="Module 1", course_id=coursez_dict["id"])
        modulez_dict = module_z.to_dict()
        module_z.save()
        data = {
            "title": "Test Project",
            "module_id": modulez_dict["id"],
            "author_id": admin.id,
            "course_id": coursez_dict["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project_z = AdminProject(**data)
        project_z.refresh()
        projectz_dict = project_z.to_dict()
        project_z.save()

        auth_response = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/{course["id"]}/project/new", headers={
            "Authorization": f"Bearer {auth_response.json.get("data").get("access_token")}"
        })
        data = response.json

        assert response.status_code == 200
        assert data["data"]["modules"]
        assert data["data"]["projects"]
        assert len(data["data"]["modules"]) == 2
        assert len(data["data"]["projects"]) == 2

def test_project_create_page_get_one_module_and_project(app, client, admin, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, projects = create_projects
        first_project = AdminProject.search(id=projects[1]["id"])
        first_project.update(next_project_id=None)
        first_project.save()
        AdminProject.search(id=projects[0]["id"]).delete()

        auth_response = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/{course["id"]}/project/new", headers={
            "Authorization": f"Bearer {auth_response.json.get("data").get("access_token")}"
        })
        data = response.json

        assert response.status_code == 200
        assert data["data"]["modules"]
        assert data["data"]["projects"]
        assert data["data"]["modules"][0]["id"] == module["id"]
        assert data["data"]["projects"][0]["id"] == projects[1]["id"]
        assert len(data["data"]["modules"]) == 1
        assert len(data["data"]["projects"]) == 1

def test_project_create_page_get_zero_module_and_project(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()

        auth_response = auth.login(admin.username, "test_password", "admin")
        response = client.get(f"/api/v1/admin/{course.id}/project/new", headers={
            "Authorization": f"Bearer {auth_response.json.get("data").get("access_token")}"
        })
        data = response.json

        assert response.status_code == 200
        assert data["data"]["modules"] == []
        assert data["data"]["projects"] == []

def test_project_create_page_get_invalid_course_id(client, admin, auth):
    auth_response = auth.login(admin.username, "test_password", "admin")
    response = client.get(f"/api/v1/admin/invalid_course_id/project/new", headers={
        "Authorization": f"Bearer {auth_response.json.get("data").get("access_token")}"
    })
    data = response.json

    assert response.status_code == 200
    assert data["data"]["modules"] == []
    assert data["data"]["projects"] == []

def test_project_create_page_get_user_not_logged_in(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()

        response = client.get(f"/api/v1/admin/{course.id}/project/new")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_project_create_page_get_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Test Course", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()

        auth_response = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/admin/{course.id}/project/new", headers={
            "Authorization": f"Bearer {auth_response.json.get("data").get("access_token")}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None