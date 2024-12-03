from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import create_access_token

from app.blueprints.auth.services import create_user, user_login, user_exists, check_specific_user_role
from app.utils.helpers import format_json_responses, handle_endpoint_exceptions

def check_user_role():
    data = check_specific_user_role()
    return format_json_responses(data=data, message="Record retrieved successfully")

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
    Registers a new user using the provided JSON data.

    This function attempts to create a new student record based on the JSON data
    received in the request. If successful, it returns a JSON response with a
    status code of 201 and a success message. If a ValueError occurs, it returns
    a JSON response with a status code of 400 and the error message. For any other
    exceptions, it returns a JSON response with a status code of 500 and the error message.

    Returns:
        Response: A Flask JSON response with the appropriate status code and message.
    """
    data = request.json
    role = data.get("role")

    if role not in ["student", "admin"]:
        raise ValueError("user role not specified")

    if role == "admin":
        if user_exists(data.get("email"), "admin"):
            raise ValueError("A user with this email already exists.")    
        user = create_user(data, "admin")

    if role == "student":
        if user_exists(data.get('email'), "student"):
            raise ValueError("A user with this email already exists.")
        user = create_user(data, "student")

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