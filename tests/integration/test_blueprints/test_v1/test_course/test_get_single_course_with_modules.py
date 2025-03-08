"""
Test cases for /api/v1/course/<course_id>/modules GET endpoint
"""


def test_get_course_with_modules_success(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dts = [
            {
                "title": "Module 1",
                "status": "published",
                "course_id": course_id,
            },
            {
                "title": "Module 2",
                "status": "published",
                "course_id": course_id,
            },
        ]
        for dt in dts:
            Module(**dt).save()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/course/{course_id}/modules", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data['data']['course']['modules']) == 2
        assert type(data['data']['course']['modules']) == list

def test_get_course_with_modules_only_one_module(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dts = [
            {
                "title": "Module 2",
                "status": "published",
                "course_id": course_id,
            },
        ]
        for dt in dts:
            Module(**dt).save()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/course/{course_id}/modules", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data['data']['course']['modules']) == 1
        assert type(data['data']['course']['modules']) == list

def test_get_course_with_modules_no_modules(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/course/{course_id}/modules", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data['data']['course']['modules']) == 0
        assert type(data['data']['course']['modules']) == list

def test_get_course_with_modules_invalid_course_id(app, client, student, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dts = [
            {
                "title": "Module 1",
                "status": "published",
                "course_id": course_id,
            },
            {
                "title": "Module 2",
                "status": "published",
                "course_id": course_id,
            },
        ]
        for dt in dts:
            Module(**dt).save()

        auth_r = auth.login(student.username, "test_password", "student")
        response = client.get(f"/api/v1/course/invalid-course-id/modules", headers={
            "Authorization": f"Bearer {auth_r.json['data']['access_token']}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_get_course_with_modules_user_logged_out(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.module import Module
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        dts = [
            {
                "title": "Module 1",
                "status": "published",
                "course_id": course_id,
            },
            {
                "title": "Module 2",
                "status": "published",
                "course_id": course_id,
            },
        ]
        for dt in dts:
            Module(**dt).save()

        response = client.get(f"/api/v1/course/{course_id}/modules")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None