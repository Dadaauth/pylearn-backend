import os
from flask_jwt_extended import create_access_token, create_refresh_token, current_user

from app.models.user import Student, Admin
from app.utils.helpers import retrieve_model_info, extract_request_data
from app.utils.error_extensions import BadRequest, InternalServerError, UnAuthenticated

def check_specific_user_role():
    data = extract_request_data("args")
    user_id = data.get("id")
    if Student.search(id=user_id) is not None:
        return {"role": "student"}
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
        user = Student.search(email=credentials.get("email"))
    elif credentials.get("role") == "admin":
        user = Admin.search(email=credentials.get("email"))

    if user is None or isinstance(user, list):
        raise BadRequest("Invalid credentials")
    if not verify_password(user, credentials.get("password")):
        raise BadRequest("Invalid credentials")
    access_token = create_access_token(identity={"id": user.id, "role": credentials.get("role")})
    refresh_token = create_refresh_token(identity={"id": user.id, "role": credentials.get("role")})
    basic_details = retrieve_model_info(user, ["id", "first_name", "last_name", "email", "role"])
    basic_details["user_id"] = basic_details.get("id")
    del basic_details["id"]
    return {"access_token": access_token, "refresh_token": refresh_token, **basic_details}

def create_user(data: dict, role: str = "student") -> dict:
    """Creates a new student record in the database
    data contains:
        - first_name, last_name, email, password (all required)
    """
    user = None
    if role == "student":
        user = Student(**data)
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
    if not credentials.get("email") or not credentials.get("password"):
        raise BadRequest("Required credentials missing")
    if credentials.get("email") == "" or credentials.get("password") == "":
        raise BadRequest("Required credentials missing")
    if not credentials.get("role") or credentials.get("role") \
        not in ["student", "admin"]:
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
        elif role == "admin":
            user = Admin.search(email=email)
        return user is not None
    except Exception as e:
        print(e)
        return False