from flask_jwt_extended import jwt_required
from app.utils.helpers import admin_required, format_json_responses, handle_endpoint_exceptions, retrieve_model_info
from .services import admin_create_new_student, all_students_data, igenerate_project_submission, igrade_student_project
from .services import iretrieve_projects_with_submissions, iretrieve_assigned_project_submissions

from app.utils.email_utils import send_email
from app.models.user import Student
import os


@jwt_required()
@admin_required
@handle_endpoint_exceptions
def grade_student_project():
    igrade_student_project()
    return format_json_responses(message="Grading successful")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def generate_project_submission(project_id):
    igenerate_project_submission(project_id)
    return format_json_responses(message="Project Submission Generated For Admin Successfully!")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_assigned_project_submissions(project_id):
    assigned_projects = iretrieve_assigned_project_submissions(project_id)
    return format_json_responses(data=assigned_projects)

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def retrieve_projects_with_submissions():
    projects = iretrieve_projects_with_submissions()
    return format_json_responses(data={"projects": projects})

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def create_new_student():
    admin_create_new_student()
    return format_json_responses(201, message="Student created successfully.")

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def fix_email_error():
    students = Student.all()
    subject = "Welcome to AuthHub! Activate Your Account Now"
    
    for student in students:
        data = student.to_dict()
        email_body = f"""
        <html>
        <body>
            <p>Dear {data.get("first_name")},</p>
            <p>Welcome to Authority Innovations Hub in partnership with GDGoC KWASU! We are excited to have you onboard as you begin this journey with us</p>
            <p>Your account has been successfully created by an administrator. To get started, you’ll need to activate your account using the details provided below:</p>
            <p><b>Your Registration Details</b></p>
            <ul>
                <li>Registration Number: {data.get("registration_number")}</li>
            </ul>
            <p><b>Account Activation</b></p>
            <p>Please click the link below to activate your account:</p>
            <p>
                <a href="{os.getenv("WEB_DOMAIN")}/auth/account/activate">Activate My Account</a>
            </p>
            <p>Once activated, you’ll have full access to your dashboard and all the resources available on our platform.</p>
            <p>If you encounter any issues during the activation process or have any questions, feel free to contact our support team at [{os.getenv("SUPPORT_EMAIL")}].</p>
            <p>We’re thrilled to have you join us and look forward to seeing you succeed!</p>
            <p>Join the whatsapp group here: <a href="https://chat.whatsapp.com/JlyU3TLSs70EWA4atfpSNf">https://chat.whatsapp.com/JlyU3TLSs70EWA4atfpSNf</a></p>
            <p>Join the discord server here: <a href="https://discord.gg/AczjSvv6">https://discord.gg/AczjSvv6</a></p>

            <p>Best regards,</p>
            <p>The AuthHub Team</p>
            <p><a href="https://authhub.tech">https://authhub.tech</a></p>
            <p>{os.getenv("SUPPORT_EMAIL")}</p>
        </body>
        </html>
        """
        send_email(data.get("email"), subject, email_body)

@jwt_required()
@admin_required
@handle_endpoint_exceptions
def all_students():
    students_data = all_students_data()
    return format_json_responses(200, data={"students": students_data})