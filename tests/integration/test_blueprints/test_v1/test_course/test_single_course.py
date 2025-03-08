"""
Test cases for /api/v1/course/<course_id> GET, UPDATE, and DELETE endpoint
"""


def test_delete_single_course_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.delete(f"/api/v1/course/{course_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
        })
        data = response.json

        assert response.status_code == 200
        assert data.get("data") is None
        assert data.get("message") == "Operation successful"
        assert Course.search(id=course_id) is None

def test_delete_single_course_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        response = client.delete(f"/api/v1/course/{course_id}")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None
        assert Course.search(id=course_id) is not None

def test_delete_single_course_user_role_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.delete(f"/api/v1/course/{course_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
        assert Course.search(id=course_id) is not None

def test_delete_single_course_invalid_course_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.delete(f"/api/v1/course/invalid-course-id", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None
        assert Course.search(id=course_id) is not None

def test_update_single_course_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/course/{course_id}",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "id": "should-not-update-id",
                "title": "Backend Web Development",
                "status": "draft"
            }
        )
        data = response.json

        assert response.status_code == 200
        assert data.get("data") is None
        assert data.get("message") == "Operation successful"
        course = Course.search(id=course_id)
        assert course.title == "Backend Web Development"
        assert course.status == "draft"
        assert course.id == course_id

def test_update_single_course_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        response = client.patch(f"/api/v1/course/{course_id}",
            json={
                "title": "Backend Web Development",
                "status": "draft"
            }
        )
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None
        course = Course.search(id=course_id)
        assert course.title == "Software Engineering"
        assert course.status == "published"

def test_update_single_course_user_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.patch(f"/api/v1/course/{course_id}",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "title": "Backend Web Development",
                "status": "draft"
            }
        )
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
        course = Course.search(id=course_id)
        assert course.title == "Software Engineering"
        assert course.status == "published"

def test_update_single_course_invalid_course_id(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.patch(f"/api/v1/course/invalid-course-id",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={
                "id": "should-not-update-id",
                "title": "Backend Web Development",
                "status": "draft"
            }
        )
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None
        course = Course.search(id=course_id)
        assert course.title == "Software Engineering"
        assert course.status == "published"

def test_get_single_course_success(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/course/{course_id}", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['course']['id'] == course_id

def test_get_single_course_invalid_course_id(client, student, auth):
    auth_r = auth.login(student.username, "test_password", "student")
    response = client.get(f"/api/v1/course/invalid-course-id", headers={
        "Authorization": f"Bearer {auth_r.json['data']['access_token']}",
    })
    data = response.json

    assert response.status_code == 404
    assert data.get("data") is None