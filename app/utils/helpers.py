"""
This module provides utility functions and decorators for a Flask application.
Functions:
    extract_request_data(type) -> dict or tuple:
    has_required_keys(dictionary: dict, required_keys: set) -> tuple:
    retrieve_model_info(obj: object, fields: list) -> dict:
    format_json_responses(status_code=200, data=None, message=None) -> tuple:
    admin_required(f: function) -> function:
    handle_endpoint_exceptions(f: function) -> function:
"""
from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import current_user

from .error_extensions import BadRequest, NotFound, UnAuthenticated


def extract_request_data(type):
    """
    Extract JSON data from the incoming request.

    Returns:
        dict: The extracted JSON data.
    """
    if type == "json":
        return request.json
    elif type == "form":
        return request.form, request.files
    elif type == "args":
        return request.args
    else:
        return None

def has_required_keys(dictionary: dict, required_keys: set):
    """
    Check if a dictionary contains all required keys.

    Args:
        dictionary (dict): The dictionary to check.
        required_keys (set): A set of keys that are required to be in the dictionary.

    Returns:
        tuple: A tuple containing a boolean and a list. The boolean is True if all required keys are present, 
               otherwise False. The list contains the missing keys if any, otherwise None.
    """
    accurate = required_keys.issubset(dictionary.keys())
    if not accurate:
        missing_keys = required_keys - dictionary.keys()
        return False, list(missing_keys)
    return True, None

def retrieve_model_info(obj: object, fields: list) -> dict:
    """
    Retrieves specified fields from an object and returns them as a dictionary.

    Args:
        obj (object): The object from which to retrieve the fields.
        fields (list): A list of field names (strings) to retrieve from the object.

    Returns:
        dict: A dictionary containing the specified fields and their corresponding values from the object.
              If a field does not exist in the object, its value will be None.
    """
    return {field: getattr(obj, field, None) for field in fields}

def format_json_responses(status_code=200, data=None, message=None):
    """
    Formats a JSON response for an HTTP request.

    Args:
        status_code (int, optional): The HTTP status code for the response. Defaults to 200.
        data (dict or list, optional): The data to include in the response. Defaults to None.
        message (str, optional): A message to include in the response. Defaults to None.

    Returns:
        tuple: A tuple containing the JSON response and the status code.
    """
    response = {
        "statusCode": status_code,
    }
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return jsonify(response), status_code



def admin_required(f):
    """
    A decorator to check if the logged-in user has an admin role.

    This decorator wraps around a function and checks if the user has an admin role.
    If the user does not have an admin role, it returns a 403 Forbidden response.

    Args:
        f (function): The endpoint function to be decorated.

    Returns:
        function: The decorated function with admin role check.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user
        if not user or user.role != 'admin':
            return format_json_responses(403, message="Forbidden: Admin access required")
        return f(*args, **kwargs)
    return decorated_function

def instructor_required(f):
    """
    A decorator to check if the logged-in user has an instructor role.

    This decorator wraps around a function and checks if the user has an instructor role.
    If the user does not have an instructor role, it returns a 403 Forbidden response.

    Args:
        f (function): The endpoint function to be decorated.

    Returns:
        function: The decorated function with instructor role check.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user
        if not user or user.role != 'instructor':
            return format_json_responses(403, message="Forbidden: Instructor access required")
        return f(*args, **kwargs)
    return decorated_function

def handle_endpoint_exceptions(f):
    """
    A decorator to handle exceptions for endpoint functions.

    This decorator wraps around a function and catches specific exceptions,
    returning formatted JSON responses with appropriate HTTP status codes.

    Args:
        f (function): The endpoint function to be decorated.

    Returns:
        function: The decorated function with exception handling.

    Raises:
        ValueError: If a ValueError is raised within the endpoint function.
        BadRequest: If a BadRequest is raised within the endpoint function.
        Exception: If any other exception is raised within the endpoint function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (ValueError, BadRequest) as e:
            return format_json_responses(400, message=str(e))
        except NotFound as e:
            return format_json_responses(404, message=str(e))
        except UnAuthenticated as e:
            return format_json_responses(401, message=str(e))
        except Exception as e:
            print(e)
            return format_json_responses(500, message="Internal Server Error")
    return decorated_function
