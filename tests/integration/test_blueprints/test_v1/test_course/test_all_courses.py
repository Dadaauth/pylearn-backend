"""
Test cases for /api/v1/course/all GET endpoint
"""
from datetime import date, timedelta


def test_get_all_courses_success(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course1 = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course2 = Course(title="Linux Essentials", status="published", communication_channel="https://discord.com/invite")
        course1.save()
        course2.save()
        Cohort(name="Cohort-1", status="in-progress", course_id=course1.id, start_date=str(date.today() + timedelta(days=13))).save()
        Cohort(name="Cohort-2", status="in-progress", course_id=course1.id, start_date=str(date.today() + timedelta(days=13))).save()
        Cohort(name="Cohort-1", status="in-progress", course_id=course2.id, start_date=str(date.today() + timedelta(days=13))).save()
        Cohort(name="Cohort-2", status="in-progress", course_id=course2.id, start_date=str(date.today() + timedelta(days=13))).save()

        response = client.get("/api/v1/course/all")
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['courses']) == list
        assert len(data['data']['courses']) == 2
        assert len(data['data']['courses'][0]['cohorts']) == 2
        assert len(data['data']['courses'][1]['cohorts']) == 2

def test_get_all_courses_one_course_no_cohort(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course1 = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course1.save()

        response = client.get("/api/v1/course/all")
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['courses']) == list
        assert len(data['data']['courses']) == 1
        assert type(data['data']['courses'][0]['cohorts']) == list
        assert len(data['data']['courses'][0]['cohorts']) == 0

def test_get_all_courses_one_course_one_cohort(app, client):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        course1 = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course1.save()
        Cohort(name="Cohort-1", status="in-progress", course_id=course1.id, start_date=str(date.today() + timedelta(days=13))).save()

        response = client.get("/api/v1/course/all")
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['courses']) == list
        assert len(data['data']['courses']) == 1
        assert type(data['data']['courses'][0]['cohorts']) == list
        assert len(data['data']['courses'][0]['cohorts']) == 1

def test_get_all_courses_no_course(app, client):
    response = client.get("/api/v1/course/all")
    data = response.json

    assert response.status_code == 404
    assert data.get("data") is None
