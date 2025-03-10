"""
Test cases for /api/v1/mentor/project/<project_id> endpoint
"""


def test_get_single_project_page_success(app, client, admin, mentor, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject
        course, module, projects = create_projects
        dt = {
            "title": "Test Project",
            "module_id": module["id"],
            "author_id": admin.id,
            "course_id": course["id"],
            "fa_duration": 2,
            "sa_duration": 1,
            "release_range": 3,
            "status": "published",
        }
        project = AdminProject(**dt)
        project.refresh()
        projects.append(project.to_dict())
        project.save()

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/mentor/project/{projects[1]["id"]}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['project']['id'] == projects[1]['id']
        assert data['data']['project']['author']['id'] == admin.id
        assert data['data']['next_project']['id'] == projects[0]['id']
        assert data['data']['prev_project']['id'] == projects[2]['id']

def test_get_single_project_page_user_not_logged_in(app, client, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        course, module, projects = create_projects

        response = client.get(f"/api/v1/mentor/project/{projects[1]["id"]}")
        data = response.json

        assert response.status_code == 401
        assert data.get('data') is None

def test_get_single_project_page_user_role_not_mentor(app, client, student, auth, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        course, module, projects = create_projects

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/mentor/project/{projects[1]["id"]}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None

def test_get_single_project_page_invalid_project_id(app, client, mentor, auth):
    with app.test_request_context():
        app.preprocess_request()

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/mentor/project/invalid-project-id", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_get_single_project_page_no_next_and_prev_project(app, client, admin, mentor, auth, create_project):
    with app.test_request_context():
        app.preprocess_request()
        course, module, project = create_project

        auth_r = auth.login(mentor.username, "test_password", "mentor")
        response = client.get(f"/api/v1/mentor/project/{project["id"]}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['project']['id'] == project['id']
        assert data['data']['project']['author']['id'] == admin.id
        assert data['data']['next_project'] is None
        assert data['data']['prev_project'] is None
