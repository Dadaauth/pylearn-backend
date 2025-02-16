
from app.models.user import Mentor
from app.utils.helpers import retrieve_model_info

def all_mentors_data():
    mentors = Mentor.all()
    mentors_data = [retrieve_model_info(mentor, ["id", \
        "first_name", "last_name",\
        "email", "status",\
        "username"])\
        for mentor in mentors]
    mentors_data = list(reversed(mentors_data))
    return mentors_data