"""
Test cases for /api/v1/admin/mentors endpoint
"""


def test_mentor_page_get_success(app, client, admin, auth):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], cohorts)
        assign_mentor_to_cohorts(mentors[1], [cohorts[0]])

        response = auth.login(admin.username, "test_password", "admin")
        response = client.get('/api/v1/admin/mentors', headers={
            "Authorization": f"Bearer {response.json["data"]["access_token"]}"
        })
        data = response.json

        assert response.status_code == 200
        assert len(data["data"]["cohorts"]) == 2
        assert len(data["data"]["mentors"]) == 2
        assert data["data"]["mentors"][0].get("password") is None
        assert data["data"]["mentors"][0]["cohorts"][0]["course"]["id"] == course["id"]
        assert data["data"]["cohorts"][0]["course"]["id"] == course["id"]

def test_mentor_page_get_zero_mentors_and_cohorts(client, admin, auth):
    response = auth.login(admin.username, "test_password", "admin")
    response = client.get('/api/v1/admin/mentors', headers={
        "Authorization": f"Bearer {response.json["data"]["access_token"]}"
    })
    data = response.json

    assert response.status_code == 200
    assert len(data["data"]["cohorts"]) == 0
    assert data["data"]["cohorts"] == []
    assert len(data["data"]["mentors"]) == 0
    assert data["data"]["mentors"] == []

def test_mentor_page_get_user_not_logged_in(app, client):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], cohorts)
        assign_mentor_to_cohorts(mentors[1], [cohorts[0]])

        response = client.get('/api/v1/admin/mentors')
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_mentor_page_get_user_role_not_admin(app, client, student, auth):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], cohorts)
        assign_mentor_to_cohorts(mentors[1], [cohorts[0]])

        response = auth.login(student.username, "test_password", "student")
        response = client.get('/api/v1/admin/mentors', headers={
            "Authorization": f"Bearer {response.json["data"]["access_token"]}"
        })
        data = response.json

        assert response.status_code == 403
        assert data.get("data") is None

def test_mentor_page_patch_success(app, client, admin, auth):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], [cohorts[0]])

        auth_response = auth.login(admin.username, "test_password", "admin")
        response = client.patch("/api/v1/admin/mentors",
            headers={"Authorization": f"Bearer {auth_response.json["data"]["access_token"]}"},
            json={
                "mentor_id": mentors[0]["id"],
                'cohorts': [cohorts[1]["id"]],
            }
        )
        data = response.json

        assert response.status_code == 200
        assert data.get("message")
        assert data.get("data") is None
        assert MentorCohort.search(mentor_id=mentors[0]["id"], cohort_id=cohorts[0]["id"]) is None
        assert MentorCohort.search(mentor_id=mentors[0]["id"], cohort_id=cohorts[1]["id"])

        response = client.patch("/api/v1/admin/mentors",
            headers={"Authorization": f"Bearer {auth_response.json["data"]["access_token"]}"},
            json={
                "mentor_id": mentors[0]["id"],
                'cohorts': [],
            }
        )
        data = response.json

        assert response.status_code == 200
        assert data.get("data") is None
        assert MentorCohort.search(mentor_id=mentors[0]["id"]) is None

def test_mentor_page_patch_user_not_logged_in(app, client):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], [cohorts[0]])

        response = client.patch("/api/v1/admin/mentors",
            json={
                "mentor_id": mentors[0]["id"],
                'cohorts': [cohorts[1]["id"]],
            }
        )
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_mentor_page_patch_user_role_not_admin(app, client, student, auth):
    from tests.utils import create_cohorts, create_mentors, assign_mentor_to_cohorts
    with app.test_request_context():
        app.preprocess_request()
        from app.models.user import MentorCohort
        course, cohorts = create_cohorts()
        mentors = create_mentors()
        assign_mentor_to_cohorts(mentors[0], [cohorts[0]])

        auth_response = auth.login(student.username, "test_password", "student")
        response = client.patch("/api/v1/admin/mentors",
            headers={"Authorization": f"Bearer {auth_response.json["data"]["access_token"]}"},
            json={
                "mentor_id": mentors[0]["id"],
                'cohorts': [cohorts[1]["id"]],
            }
        )
        data = response.json

        assert response.status_code == 403
        assert data.get("message")
        assert data.get("data") is None