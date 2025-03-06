from datetime import date, timedelta

def create_user(client, data):
    return client.post("/api/v1/auth/register", json=data)

def create_cohorts():
    from app.models.course import Course
    from app.models.cohort import Cohort
    course = Course(title="Software Engineering",
        status="published",
        communication_channel="https://discord.com/invite"
    )
    course_dict = course.to_dict()
    course.save()
    data = [
        {
            "name": "Cohort-1",
            "status": "completed",
            "course_id": course_dict["id"],
            "start_date": date.today() - timedelta(days=80)
        },
        {
            "name": "Cohort-2",
            "status": "in-progress",
            "course_id": course_dict["id"],
            "start_date": date.today() - timedelta(days=40)
        },
    ]
    cohorts = []
    for dt in data:
        cohort = Cohort(**dt)
        cohort.refresh()
        cohorts.append(cohort.to_dict())
    return course_dict, cohorts

def create_mentors():
    from app.models.user import Mentor
    data = [
        {
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "email": "mentor@email.com",
            "username": "test_mentor1",
        },
        {
            "first_name": "Test",
            "last_name": "Last",
            "password": "test_password",
            "email": "mentor2@email.com",
            "username": "test_mentor12",
        },
    ]
    mentors = []
    for dt in data:
        mentor = Mentor(**dt)
        mentors.append(mentor.to_dict())
        mentor.save()
    return mentors

def assign_mentor_to_cohorts(mentor: dict, cohorts: list[dict]) -> None:
    from app.models.user import Mentor, MentorCohort
    from app.models.cohort import Cohort
    mentor = Mentor.search(id=mentor["id"])
    for cohort in cohorts:
        if not Cohort.search(id=cohort["id"]): continue
        MentorCohort(mentor_id=mentor.id, cohort_id=cohort["id"]).save()