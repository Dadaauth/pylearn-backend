"""
Test cases for /api/v1/course/create POST endpoint
"""


def test_course_create_success(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.post("/api/v1/course/create",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={"title": "Software Engineering", "communication_channel": "https://discord.com/invite"},
        )
        data = response.json

        assert response.status_code == 201
        assert data.get("message") == "Course creation successful"
        assert data.get("data") is None
        course = Course.all()
        assert course is not None
        assert course[0].title == "Software Engineering"

def test_course_create_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        response = client.post("/api/v1/course/create",
            json={"title": "Software Engineering", "communication_channel": "https://discord.com/invite"},
        )
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None
        course = Course.all()
        assert course == []

def test_course_create_user_not_admin(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        auth_r = auth.login(student.username, "test_password", "student")
        response = client.post("/api/v1/course/create",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={"title": "Software Engineering", "communication_channel": "https://discord.com/invite"},
        )
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
        # it's 1 because a course was created when creating the student account
        assert len(Course.all()) == 1

def test_course_create_required_fields_absent(app, client, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        auth_r = auth.login(admin.username, "test_password", "admin")
        response = client.post("/api/v1/course/create",
            headers={"Authorization": f"Bearer {auth_r.json['data']['access_token']}"},
            json={},
        )
        data = response.json

        assert response.status_code == 400
        assert data.get("message") == "Required field(s) (title or communication_channel) absent in request"
        assert data.get("data") is None
        course = Course.all()
        assert course == []