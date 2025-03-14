"""
Test cases for /api/v1/student/project/<project_id> GET endpoint
"""
from datetime import date, timedelta


def test_student_get_single_project_page_success(app, client, admin, create_projects, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject, CohortProject, StudentProject
        from app.models.cohort import Cohort
        from app.models.user import Student
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
        # Create Cohort
        cohort = Cohort(
            name="Cohort-1",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=25),
        )
        cohort.refresh()
        # Create Student
        student = Student(
            first_name="Test",
            last_name="Student",
            email="student1@emai.com",
            username="test_student1",
            password="test_password",
            cohort_id=cohort.id,
            course_id=course['id'],
        )
        student.save()
        student.refresh()
        # create CohortProject (s)
        cohort_projects = []
        for project in projects:
            cohort_project = CohortProject(
                title=project['title'],
                module_id=project['module_id'],
                author_id=project['author_id'],
                course_id=project['course_id'],
                fa_start_date=date.today() - timedelta(days=6),
                sa_start_date=date.today() - timedelta(days=3),
                end_date=date.today() + timedelta(days=1),
                status="second-attempt",
                cohort_id=cohort.id,
                project_pool_id=project['id'],
            )
            cohort_project.save()
            cohort_project.refresh()
            cohort_projects.append(cohort_project.to_dict())
        # Create StudentProject
        student_project = StudentProject(
            status="submitted",
            submitted_on=date.today(),
            student_id=student.id,
            cohort_id=cohort.id,
            cohort_project_id=cohort_projects[0]['id'],
        )
        student_project.save()
        student_project.refresh()

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        response = client.get(f"/api/v1/student/project/{cohort_projects[1]['id']}", headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['project']['id'] == cohort_projects[1]['id']
        assert data['data']['project']['module']['id'] == module['id']
        assert data['data']['project']['author']
        assert data['data']['project']['status'] == "second-attempt"
        assert data['data']['next_project']['id'] == cohort_projects[0]['id']
        assert data['data']['next_project']['status'] == "submitted"
        assert data['data']['next_project']['module']['id'] == module['id']
        assert data['data']['prev_project']['id'] == cohort_projects[2]['id']
        assert data['data']['prev_project']['status'] == "second-attempt"
        assert data['data']['prev_project']['module']['id'] == module['id']

def test_student_get_single_project_page_user_logged_out(app, client, admin, create_projects):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject, CohortProject, StudentProject
        from app.models.cohort import Cohort
        from app.models.user import Student
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
        # Create Cohort
        cohort = Cohort(
            name="Cohort-1",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=25),
        )
        cohort.refresh()
        # Create Student
        student = Student(
            first_name="Test",
            last_name="Student",
            email="student1@emai.com",
            username="test_student1",
            password="test_password",
            cohort_id=cohort.id,
            course_id=course['id'],
        )
        student.save()
        student.refresh()
        # create CohortProject (s)
        cohort_projects = []
        for project in projects:
            cohort_project = CohortProject(
                title=project['title'],
                module_id=project['module_id'],
                author_id=project['author_id'],
                course_id=project['course_id'],
                fa_start_date=date.today() - timedelta(days=6),
                sa_start_date=date.today() - timedelta(days=3),
                end_date=date.today() + timedelta(days=1),
                status="second-attempt",
                cohort_id=cohort.id,
                project_pool_id=project['id'],
            )
            cohort_project.save()
            cohort_project.refresh()
            cohort_projects.append(cohort_project.to_dict())
        # Create StudentProject
        student_project = StudentProject(
            status="submitted",
            submitted_on=date.today(),
            student_id=student.id,
            cohort_id=cohort.id,
            cohort_project_id=cohort_projects[0]['id'],
        )
        student_project.save()
        student_project.refresh()

        response = client.get(f"/api/v1/student/project/{cohort_projects[1]['id']}")
        data = response.json

        assert response.status_code == 401
        assert data.get("data") is None

def test_student_get_single_project_page_invalid_project_id(app, client, admin, create_projects, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject, CohortProject, StudentProject
        from app.models.cohort import Cohort
        from app.models.user import Student
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
        # Create Cohort
        cohort = Cohort(
            name="Cohort-1",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=25),
        )
        cohort.refresh()
        # Create Student
        student = Student(
            first_name="Test",
            last_name="Student",
            email="student1@emai.com",
            username="test_student1",
            password="test_password",
            cohort_id=cohort.id,
            course_id=course['id'],
        )
        student.save()
        student.refresh()
        # create CohortProject (s)
        cohort_projects = []
        for project in projects:
            cohort_project = CohortProject(
                title=project['title'],
                module_id=project['module_id'],
                author_id=project['author_id'],
                course_id=project['course_id'],
                fa_start_date=date.today() - timedelta(days=6),
                sa_start_date=date.today() - timedelta(days=3),
                end_date=date.today() + timedelta(days=1),
                status="second-attempt",
                cohort_id=cohort.id,
                project_pool_id=project['id'],
            )
            cohort_project.save()
            cohort_project.refresh()
            cohort_projects.append(cohort_project.to_dict())
        # Create StudentProject
        student_project = StudentProject(
            status="submitted",
            submitted_on=date.today(),
            student_id=student.id,
            cohort_id=cohort.id,
            cohort_project_id=cohort_projects[0]['id'],
        )
        student_project.save()
        student_project.refresh()

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        response = client.get("/api/v1/student/project/invalid-project-id", headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 404
        assert data.get("data") is None

def test_student_get_single_project_page_no_next_project_no_previous_project(app, client, admin, create_project, auth):
    with app.test_request_context():
        app.preprocess_request()
        from app.models.project import AdminProject, CohortProject, StudentProject
        from app.models.cohort import Cohort
        from app.models.user import Student
        course, module, project = create_project
        # Create Cohort
        cohort = Cohort(
            name="Cohort-1",
            course_id=course['id'],
            start_date=date.today() - timedelta(days=25),
        )
        cohort.refresh()
        # Create Student
        student = Student(
            first_name="Test",
            last_name="Student",
            email="student1@emai.com",
            username="test_student1",
            password="test_password",
            cohort_id=cohort.id,
            course_id=course['id'],
        )
        student.save()
        student.refresh()
        # create CohortProject
        cohort_project = CohortProject(
            title=project['title'],
            module_id=project['module_id'],
            author_id=project['author_id'],
            course_id=project['course_id'],
            fa_start_date=date.today() - timedelta(days=6),
            sa_start_date=date.today() - timedelta(days=3),
            end_date=date.today() + timedelta(days=1),
            status="second-attempt",
            cohort_id=cohort.id,
            project_pool_id=project['id'],
        )
        cohort_project.save()
        cohort_project.refresh()
        cohort_project_id = cohort_project.id

        token = auth.login(student.username, "test_password", "student").json['data']['access_token']
        response = client.get(f"/api/v1/student/project/{cohort_project_id}", headers={
            "Authorization": f"Bearer {token}"
        })
        data = response.json

        assert response.status_code == 200
        assert data['data']['project']['id'] == cohort_project_id
        assert data['data']['project']['module']['id'] == module['id']
        assert data['data']['project']['author']
        assert data['data']['project']['status'] == "second-attempt"
        assert data['data']['next_project'] is None
        assert data['data']['prev_project'] is None
