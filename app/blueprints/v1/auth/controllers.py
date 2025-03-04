import os

from flask import request
from flask_jwt_extended import get_current_user, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import create_access_token

from app.blueprints.v1.auth.services import create_user, user_login, user_exists, check_specific_user_role
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions, retrieve_model_info
from jobs.tasks.jobs import send_transactional_email

@jwt_required()
def check_user_role():
    identity = get_jwt_identity()
    return format_json_responses(data={"role": identity["role"]}, message="Record retrieved successfully")

@jwt_required()
def get_user_details():
    """
    Fetches basic details of the currently logged-in user.

    This function requires a valid JWT token to be present in the request.
    If the token is valid, it retrieves the user's identity and returns
    a JSON response with the user's details.

    Returns:
        Response: A JSON response containing the user's details.
    """
    current_user = get_current_user()
    return format_json_responses(data=current_user.basic_info(), message="User details retrieved successfully")

@jwt_required()
def is_logged_in():
    """
    Checks if the user is currently logged in by verifying the JWT token.

    This function requires a valid JWT token to be present in the request.
    If the token is valid, it returns a JSON response indicating that the user
    is logged in.

    Returns:
        Response: A JSON response indicating the login status of the user.
    """
    current_user = get_jwt_identity()
    return format_json_responses(data={"user": current_user}, message="User is logged in")

@handle_endpoint_exceptions
def login():
    """
    Handles user login by processing the provided JSON data and returning a token.

    This function extracts JSON data from the request, attempts to log in the user
    using the provided data, and returns a formatted JSON response with a token
    and a success message.

    Returns:
        Response: A JSON response containing the authentication token and a success message.
    """
    data = request.json
    dt = user_login(data)
    return format_json_responses(data=dt, message="User logged in successfully!")

@jwt_required(optional=True)
@handle_endpoint_exceptions
def register():
    """
    Registers a new user (admin and mentor only) using the provided JSON data.

    This function attempts to create a new user record based on the JSON data
    received in the request. If successful, it returns a JSON response with a
    status code of 201 and a success message. If a ValueError occurs, it returns
    a JSON response with a status code of 400 and the error message. For any other
    exceptions, it returns a JSON response with a status code of 500 and the error message.

    Returns:
        Response: A Flask JSON response with the appropriate status code and message.
    """
    data = request.json
    role = data.get("role")

    if role not in ["mentor", "admin"]:
        raise ValueError("user role not specified")

    if role == "admin":
        if user_exists(data.get("email"), "admin"):
            raise ValueError("A user with this email already exists.")    
        user = create_user(data, "admin")

    if role == "mentor":
        if user_exists(data.get('email'), "mentor"):
            raise ValueError("A user with this email already exists.")
        user = create_user(data, "mentor")
        subject = f"Welcome to PyLearn, {user["first_name"]}! Activate Your Account 🚀"
        htmlBody = f"""
        <b>Hi {{mentor_name}},</b>
        <br/><br/>
        Welcome to <b>PyLearn! 🎉</b> Your mentor account has been created by an admin, and we’re excited to have you on board.
        <br/>
        To get started, please activate your account by clicking the link below:
        <br/>
        <a href="{os.getenv("FRONTEND_URL")}/auth/account/mentor/activate">🔗 Activate Account</a>
        <br/>
        Or copy and paste this link in the browser: {os.getenv("FRONTEND_URL")}/auth/account/mentor/activate"
        <br/><br/>
        Once activated, you’ll be able to access your dashboard, connect with students, and start mentoring right away!
        <br/>
        If you have any questions, feel free to reach out to us.
        <br/><br/>
        Looking forward to an amazing journey together! 🚀
        <br/><br/>
        Best,<br/>
        The PyLearn Team<br/>
        {os.getenv("SUPPORT_EMAIL")}
        """
        receipient_email = user["email"]
        send_transactional_email.delay(subject, htmlBody, receipient_email)

    return format_json_responses(201,
                                data={
                                    "user": user
                                }, message="User registered successfully!")

@jwt_required(optional=True)
def logout():
    """
    Logs out the current user by unsetting JWT cookies and returning a formatted JSON response.
    This function performs the following actions:
    1. Formats a JSON response with a message indicating successful logout.
    2. Unsets the JWT cookies in the response to effectively log out the user.
    3. Returns the formatted response.
    Todo:
        add revoked tokens to blocklist in storage.
    Returns:
        response (tuple): A tuple containing the HTTP response object and status code.
    """
    
    response = format_json_responses(message="User logged out successfully!")
    unset_jwt_cookies(response[0])
    return response

@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return format_json_responses(data={"access_token": new_token},
                                 message="Token refreshed successfully!")