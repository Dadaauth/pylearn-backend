"""
Test cases for /api/v1/course/<course_id>/all GET endpoint
"""
from datetime import date, timedelta


def test_get_all_course_data_success(app, client, admin):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.module import Module
        from app.models.project import AdminProject
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort_dts = [
            {
                "name": "Cohort-1",
                "status": "in-progress",
                "course_id": course_id,
                "start_date": date.today() + timedelta(days=12),
            },
            {
                "name": "Cohort-2",
                "status": "in-progress",
                "course_id": course_id,
                "start_date": date.today() + timedelta(days=12),
            }
        ]
        for cohort_dt in cohort_dts:
            Cohort(**cohort_dt).save()
        module_dts = [
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
        modules = []
        for module_dt in module_dts:
            module = Module(**module_dt)
            modules.append(module.to_dict())
            module.save()
        project_dts = [
            {
                "title": "Project 1",
                "module_id": modules[0]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
            {
                "title": "Project 1",
                "module_id": modules[0]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
            {
                "title": "Project 1",
                "module_id": modules[1]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
        ]
        for project_dt in project_dts:
            AdminProject(**project_dt).save()

        response = client.get(f"/api/v1/course/{course_id}/all")
        data = response.json

        assert response.status_code == 200
        assert type(data['data']['course']['modules']) == list
        assert len(data['data']['course']['modules']) == 2
        assert type(data['data']['course']['modules'][0]['projects']) == list
        assert type(data['data']['course']['modules'][1]['projects']) == list
        assert type(data['data']['course']['cohorts']) == list
        assert len(data['data']['course']['cohorts']) == 2

def test_get_all_course_data_invalid_course_id(app, client, admin):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.course import Course
        from app.models.cohort import Cohort
        from app.models.module import Module
        from app.models.project import AdminProject
        course = Course(title="Software Engineering", status="published", communication_channel="https://discord.com/invite")
        course.save()
        course.refresh()
        course_id = course.id
        cohort_dts = [
            {
                "name": "Cohort-1",
                "status": "in-progress",
                "course_id": course_id,
                "start_date": date.today() + timedelta(days=12),
            },
            {
                "name": "Cohort-2",
                "status": "in-progress",
                "course_id": course_id,
                "start_date": date.today() + timedelta(days=12),
            }
        ]
        for cohort_dt in cohort_dts:
            Cohort(**cohort_dt).save()
        module_dts = [
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
        modules = []
        for module_dt in module_dts:
            module = Module(**module_dt)
            modules.append(module.to_dict())
            module.save()
        project_dts = [
            {
                "title": "Project 1",
                "module_id": modules[0]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
            {
                "title": "Project 1",
                "module_id": modules[0]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
            {
                "title": "Project 1",
                "module_id": modules[1]['id'],
                "author_id": admin.id,
                "course_id": course_id,
                "status": "published",
                "fa_duration": 3,
                "sa_duration": 5,
                "release_range": 6,
            },
        ]
        for project_dt in project_dts:
            AdminProject(**project_dt).save()

        response = client.get(f"/api/v1/course/invalid-course-id/all")
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None