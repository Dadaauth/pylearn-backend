import os
from uuid import uuid4
from flask_jwt_extended import create_access_token, create_refresh_token, current_user, get_jwt_header, get_jwt_identity

from app.models.user import Student, Admin, Mentor
from app.models.cohort import Cohort
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, InternalServerError, UnAuthenticated

def check_specific_user_role():
    data = extract_request_data("args")
    user_id = data.get("id")
    if Student.search(id=user_id) is not None:
        return {"role": "student"}
    if Mentor.search(id=user_id) is not None:
        return {"role": "mentor"}
    if Admin.search(id=user_id) is not None:
        return {"role": "admin"}

def user_login(credentials):
    """
    Authenticates a user based on provided credentials.

    Args:
        credentials (dict): A dictionary containing the user's email and password.

    Raises:
        BadRequest: If the credentials are invalid or the user is not found.

    Returns:
        dict: A dictionary containing the access token if authentication is successful.
    """
    check_credentials(credentials)
    user = None
    if credentials.get("role") == "student":
        user = Student.search(username=credentials.get("username"))
    elif credentials.get("role") == "mentor":
        user = Mentor.search(username=credentials.get("username"))
    elif credentials.get("role") == "admin":
        user = Admin.search(username=credentials.get("username"))

    if user is None or isinstance(user, list):
        raise BadRequest("Invalid credentials")
    if user.status != "active":
        raise BadRequest("Account not yet activated")
    if not verify_password(user, credentials.get("password")):
        raise BadRequest("Invalid credentials")
    
    if isinstance(user, Student):
        if not user.cohort_id:
            raise BadRequest("Student not assigned to cohort")
        cohort = Cohort.search(id=user.cohort_id)
        if not cohort:
            raise BadRequest("Student not assigned to cohort")
        if cohort.status == "pending":
            raise BadRequest("Student Cohort is not yet active")
        
    if user.status != "active":
        raise BadRequest("User account is not yet active")

    access_token = create_access_token(identity={"id": user.id, "role": credentials.get("role")})
    refresh_token = create_refresh_token(identity={"id": user.id, "role": credentials.get("role")})
    basic_details = retrieve_model_info(user, ["id", "first_name", "last_name", "email", "username"])
    basic_details["role"] = credentials.get("role")
    basic_details["user_id"] = basic_details.get("id")
    del basic_details["id"]
    return {"access_token": access_token, "refresh_token": refresh_token, **basic_details}

def verify_is_admin(id):
    admin = Admin.search(id=id)
    if admin is None:
        raise UnAuthenticated("Only Admins can register mentor accounts")

def create_user(data: dict, role: str) -> dict:
    """Creates a new user record in the database
    data contains:
        - first_name, last_name, email, password (all required)
    """
    user = None
    if role == "mentor":
        verify_is_admin(get_jwt_identity()["id"])
        details = {
            "email": data.get('email'),
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "password": "placeholder",
            "username": str(uuid4()),
            "status": "inactive",
        }
        user = Mentor(**details)
    elif role == "admin":
        if data.get("admin_reg_code") != os.getenv("ADMIN_REGISTRATION_PASSCODE"):
            raise UnAuthenticated("Invalid admin registration passcode")
        user = Admin(**data)
    else:
        raise InternalServerError
    user.add()
    user.save()
    user.refresh()
    fields = {"id", "first_name", "last_name",\
              "email", "role"}
    return retrieve_model_info(user, fields)


def check_credentials(credentials: dict) -> None:
    """Checks if the required credentials are present in the request data."""
    if not credentials.get("username") or not credentials.get("password"):
        raise BadRequest("Required credentials missing")
    if credentials.get("username") == "" or credentials.get("password") == "":
        raise BadRequest("Required credentials missing")
    if not credentials.get("role") or credentials.get("role") \
        not in ["student", "mentor", "admin"]:
        raise BadRequest("Invalid role")
    
def verify_password(user, password: str) -> bool:
    """Verifies if the provided password matches the user's password."""
    return user.check_password(password)

def user_exists(email: str, role: str ="student") -> bool:
    """Checks if a user with the given email exists in the database."""
    try:
        user = None
        if role == "student":
            user = Student.search(email=email)
        elif role == "mentor":
            user = Mentor.search(email=email)
        elif role == "admin":
            user = Admin.search(email=email)
        return user is not None
    except Exception as e:
        print(e)
        return False