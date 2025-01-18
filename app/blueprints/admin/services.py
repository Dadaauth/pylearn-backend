from datetime import datetime, timezone
from uuid import uuid4

from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import extract_request_data, retrieve_model_info
from app.utils.error_extensions import BadRequest, NotFound
from app.models.user import Student
from app.models.project import StudentProject, Project
from app.utils.email_utils import send_email

def igrade_student_project():
    data = extract_request_data("json")
    admin_id = get_jwt_identity()["id"]

    if not data.get("student_project_id") or not data.get("grade"):
        raise BadRequest("Required field(s): student_project_id, grade not present")

    studentProject = StudentProject.search(id=data.get("student_project_id"))
    if not studentProject:
        raise NotFound("Student's project not found")
    
    studentProject.status = "graded"
    studentProject.graded_on = datetime.now(timezone.utc)
    studentProject.graded_by = admin_id
    studentProject.grade = data.get("grade")
    studentProject.feedback = data.get('feedback')
    studentProject.save()

def iretrieve_assigned_project_submissions(project_id):
    admin_id = get_jwt_identity()["id"]
    project = Project.search(id=project_id)
    assigned_pjts = StudentProject.search(status="submitted", project_id=project_id, assigned_to=admin_id)

    if not assigned_pjts:
        raise NotFound("No submitted projects")

    tmp = []
    if isinstance(assigned_pjts, StudentProject):
        tmp.append(assigned_pjts)
    elif isinstance(assigned_pjts, list):
        for pjt in assigned_pjts:
            tmp.append(pjt)

    assigned_projects = {
        "project": project.to_dict(),
        "data": [],
    }
    for t in tmp:
        student = Student.search(id=t.student_id)
        data = {
            "student": student.to_dict(),
            "student_project": t.to_dict(),
        }
        assigned_projects.get("data").append(data)
    return assigned_projects

def iretrieve_projects_with_submissions():
    submissions = StudentProject.search(status="submitted")
    if not submissions:
        raise NotFound("No Submitted Projects Found")

    """Check how many projects were found"""
    if isinstance(submissions, StudentProject):
        submissions = [submissions]

    projects_with_submissions = []
    projects_with_submissions_registry = []
    for submission in submissions:
        if submission.project_id in projects_with_submissions_registry:
            continue
        project = Project.search(id=submission.project_id)
        if not Project: continue
        projects_with_submissions_registry.append(project.id)
        projects_with_submissions.append(project.to_dict())

    return projects_with_submissions

def igenerate_project_submission(project_id):
    admin_id = get_jwt_identity()["id"]
    submitted_projects = StudentProject.search(project_id=project_id, status="submitted", assigned_to=None)
    if not submitted_projects:
        raise NotFound("No Submitted Projects")

    """Check how many projects were found"""
    if isinstance(submitted_projects, StudentProject):
        submitted_projects.assigned_to = admin_id
        submitted_projects.save()
    elif isinstance(submitted_projects, list):
        submitted_projects[0].assigned_to = admin_id
        submitted_projects[0].save()

def all_students_data():
    students = Student.all()
    students_data = [retrieve_model_info(student, ["id", \
                                                   "first_name", "last_name",\
                                                    "email", "registration_number", "status",\
                                                    "username"])\
                    for student in students]
    students_data = list(reversed(students_data))
    return students_data

def admin_create_new_student():
    data = extract_request_data("json")
    if not (data.get("first_name") and data.get("last_name") and data.get("email")):
        raise BadRequest("Missing required field(s): first_name, last_name, email")
    
    student_count = Student.count() + 1
    registration_number = f"{datetime.now().year}/SWE/C1/{str(student_count).zfill(4)}"
    student_details = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "username": str(uuid4()),
        "password": "placeholder",
        "status": "inactive",
        "registration_number": registration_number
    }
    Student(**student_details).save()
    subject = "Welcome to AuthHub! Activate Your Account Now"
    email_body = f"""
    <html>
    <body>
        <p>Dear {data.get("first_name")},</p>
        <p>Welcome to Authority Innovations Hub! We are excited to have you onboard as you begin this journey with us</p>
        <p>Your account has been successfully created by an administrator. To get started, you’ll need to activate your account using the details provided below:</p>
        <p><b>Your Registration Details</b></p>
        <ul>
            <li>Registration Number: {registration_number}</li>
        </ul>
        <p><b>Account Activation</b></p>
        <p>Please click the link below to activate your account:</p>
        <p><a href="http://localhost:3000/auth/account/activate?reg_no={registration_number}">Activate My Account</a>
        </p>
        <p>Once activated, you’ll have full access to your dashboard and all the resources available on our platform.</p>
        <p>If you encounter any issues during the activation process or have any questions, feel free to contact our support team at [support@authhub.tech].</p>
        <p>We’re thrilled to have you join us and look forward to seeing you succeed!</p>

        <p>Best regards,</p>
        <p>The AuthHub Team</p>
        <p>https://authhub.tech</p>
        <p>support@authhub.tech</p>
    </body>
    </html>
    """
    send_email(data.get("email"), subject, email_body)