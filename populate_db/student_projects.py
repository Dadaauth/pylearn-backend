# """
# Populate your database
# """
# import random
# from datetime import datetime, timezone

# from app.models.user import Student, Mentor
# from app.models.cohort import Cohort
# from app.models.project import CohortProject, StudentProject


# def populate_student_projects():
#     cohorts = Cohort.all()
#     mentors = Mentor.all()
#     for cohort in cohorts:
#         print(CohortProject.count(cohort_id=cohort.id))
#         projects = CohortProject.search(cohort_id=cohort.id)
#         students = Student.search(cohort_id=cohort.id)
#         for student in students:
#             # Create projects for single student
#             print(student)
#             for project in projects:
#                 status = random.choice(["submitted", "graded", "verified"])
#                 assigned_to = random.choice(mentors).id
#                 graded_on = datetime.now(timezone.utc) if status != "submitted" else None
#                 grade = random.randint(0, 100) if status != "submitted" else None
#                 feedback = "This is Awesome!" if status != "submitted" else None
#                 StudentProject(
#                     cohort_id=cohort.id,
#                     student_id=student.id,
#                     cohort_projects_id=project.id,
#                     status=status,
#                     submission_file="https://google.com",
#                     assigned_to=assigned_to,
#                     graded_on=graded_on,
#                     graded_by=assigned_to,
#                     grade=grade,
#                     feedback=feedback
#                 ).save()
#     print("Student Projects successfully populated")
