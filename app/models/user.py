from sqlalchemy import Integer, String, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from flask_bcrypt import generate_password_hash, check_password_hash

from app.models.basemodel import BaseModel
from app.models.base import Base
from app.utils.helpers import has_required_keys


class User(BaseModel):
    """
        User Model
        Attributes:
            first_name (str): The first name of the user. Must be a non-null string with a maximum length of 300 characters.
            last_name (str): The last name of the user. Must be a non-null string with a maximum length of 300 characters.
            email (str): The email address of the user. Must be a non-null string with a maximum length of 300 characters.
            password (str): The password of the user. Must be a non-null string stored as a hashed value.
            role (str): The role of the user. Must be one of 'admin' or 'student'. Defaults to 'student'.
        Methods:
            __init__(**kwargs): Initializes a User instance with the provided keyword arguments. Raises a ValueError if any required keys are missing.
            basic_info() -> dict: Returns a dictionary containing basic information about the user, including id, first_name, last_name, and email.
    """
    first_name = mapped_column(String(60), nullable=False)
    last_name = mapped_column(String(60), nullable=False)
    password = mapped_column(String(300), nullable=False)
    email = mapped_column(String(255), nullable=False, unique=True)
    username = mapped_column(String(60), nullable=False, unique=True)
    phone = mapped_column(String(45))
    status = mapped_column(Enum("active", "inactive", "suspended", "deleted"), default="active", nullable=False)

    def __init__(self, **kwargs):
        """
            Initialize a new User instance.
            Args:
                **kwargs: Arbitrary keyword arguments containing user attributes.
            Raises:
                ValueError: If any of the required keys ('first_name', 'last_name', 'email', 'password') are missing.
            Attributes:
                password (str): The hashed password of the user.
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {'first_name', 'last_name', 'email', 'password', "username"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required keys: {', '.join(missing)}")

        self.password = generate_password_hash(self.password).decode()

    def update(self, **kwargs):
        if kwargs.get("password"):
            setattr(self, "password", generate_password_hash(kwargs["password"]))
            del kwargs["password"]
        super().update(**kwargs)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the user's password.

        Args:
            password (str): The password to check against the user's password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return check_password_hash(self.password, password)

    def basic_info(self) -> dict:
        """
        Returns a dictionary containing the basic information of the user.

        Returns:
            dict: A dictionary with the user's id, first name, last name, and email.
        """
        info = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }
        return info


class Admin(User, Base):
    """
    Admin class that inherits from User and Base.
    Attributes:
        __tablename__ (str): The name of the table in the database.
    Methods:
        __init__(**kwargs): Initializes an Admin instance with given keyword arguments.
    """
    __tablename__ = "admins"

    def __init__(self, **kwargs):
        """
        Initialize a new User instance with the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass initializer.
        """
        super().__init__(**kwargs)

class Mentor(User, Base):
    """
    Mentor class that inherits from User and Base.
    Attributes:
        __tablename__ (str): The name of the table in the database.
    Methods:
        __init__(**kwargs): Initializes a Mentor instance with given keyword arguments.
    """
    __tablename__ = "mentors"
    # TODO: create a table for many to many relationships between cohorts and mentors
    #   This table will also determine the course the Mentor can access since each
    #   cohort binds itself to a particular course.

    def __init__(self, **kwargs):
        """
        Initialize a new User instance with the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass initializer.
        """
        super().__init__(**kwargs)

class Student(User, Base):
    """
    Represents a student in the system.
    Attributes:
        __tablename__ (str): The name of the table in the database.
    Methods:
        __init__(**kwargs): Initializes a new instance of the Student class.
    """
    __tablename__ = "students"
    points = mapped_column(Integer, nullable=False, default=0)
    registration_number = mapped_column(String(100), nullable=False)
    # cohort already contains the course the student is taking
    cohort_id = mapped_column(ForeignKey("cohorts.id"))

    cohort = relationship("Cohort", back_populates="students")

    def __init__(self, **kwargs):
        """
        Initialize a new instance of the class.

        Parameters:
        **kwargs: Arbitrary keyword arguments passed to the superclass initializer.
        """
        super().__init__(**kwargs)

        required_keys = {"registration_number"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")