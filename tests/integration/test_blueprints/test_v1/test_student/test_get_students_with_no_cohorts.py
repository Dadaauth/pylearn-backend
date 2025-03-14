"""
Test cases for /api/v1/student/no-cohort/<course_id> GET endpoint
"""


def test_get_students_with_no_cohort_success(app, client, students, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        students[0].cohort_id = None
        students[0].save()
        students[1].cohort_id = None
        students[1].save()
        students[0].refresh()
        course_id = students[0].course_id

        token = auth.login(admin.username, "test_password", "admin").json['data']['access_token']
        response = client.get(f'/api/v1/student/no-cohort/{course_id}', headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']["students"]) == list
        assert len(data['data']["students"]) == 2
        assert data['data']["students"][0]['email']
        assert data['data']["students"][0]['username']
        assert data['data']["students"][0]['last_name']
        assert data['data']["students"][0]['id']
        assert data['data']["students"][0].get("password") is None
        assert data['data']["students"][1].get("password") is None

def test_get_students_with_no_cohort_one_student(app, client, student, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        student.cohort_id = None
        student.save()
        student.refresh()
        course_id = student.course_id
        student_id = student.id

        token = auth.login(admin.username, "test_password", "admin").json['data']['access_token']
        response = client.get(f'/api/v1/student/no-cohort/{course_id}', headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']["students"]) == list
        assert len(data['data']["students"]) == 1
        assert data['data']["students"][0]['id'] == student_id
        assert data['data']["students"][0].get("password") is None

def test_get_students_with_no_cohort_no_students(app, client, create_course, admin, auth):
    with app.test_request_context():
        app.preprocess_request()
        course = create_course

        token = auth.login(admin.username, "test_password", "admin").json['data']['access_token']
        response = client.get(f'/api/v1/student/no-cohort/{course['id']}', headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 200
        assert type(data['data']["students"]) == list
        assert len(data['data']["students"]) == 0

def test_get_students_with_no_cohort_user_logged_out(app, client, student):
    with app.test_request_context():
        app.preprocess_request()
        student.cohort_id = None
        student.save()
        student.refresh()
        course_id = student.course_id

        response = client.get(f'/api/v1/student/no-cohort/{course_id}')
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_get_students_with_no_cohort_user_role_not_admin(app, client, student, mentor, auth):
    with app.test_request_context():
        app.preprocess_request()
        student.cohort_id = None
        student.save()
        student.refresh()
        course_id = student.course_id
        student_id = student.id

        token = auth.login(mentor.username, "test_password", "mentor").json['data']['access_token']
        response = client.get(f'/api/v1/student/no-cohort/{course_id}', headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None
