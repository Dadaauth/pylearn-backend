"""
Database population will be started from here.
All the populated data will be saved to a dump file (report.txt)
"""
import os
import sys

sys.path.insert(0, os.getcwd())

from app import create_app, g
from app.models import storage

from admins import populate_admins
from courses import populate_courses
from cohorts import populate_cohorts
from students import populate_students
from mentors import populate_mentors
from modules import populate_modules
from admin_projects import populate_admin_projects

app = create_app()

COURSES_CSV_FILE = "populate_db/csv/courses.csv"
ADMINS_CSV_FILE = "populate_db/csv/admins.csv"
COHORTS_CSV_FILE = "populate_db/csv/cohorts.csv"
STUDENTS_CSV_FILE = "populate_db/csv/students.csv"
MENTORS_CSV_FILE = "populate_db/csv/mentors.csv"
MODULES_CSV_FILE = "populate_db/csv/modules.csv"
ADMINS_PROJECTS_CSV_FILE = "populate_db/csv/admin_projects.csv"
COHORT_PROJECTS_CSV_FILE = "populate_db/csv/cohort_projects.csv"

os.makedirs("populate_db/csv", exist_ok=True)

with app.app_context():
    storage.load()
    g.db_storage = storage
    
    populate_admins(ADMINS_CSV_FILE)
    print()
    populate_courses(COURSES_CSV_FILE)
    print()
    populate_cohorts(COURSES_CSV_FILE, COHORTS_CSV_FILE)
    print()
    populate_students(COHORTS_CSV_FILE, STUDENTS_CSV_FILE)
    print()
    populate_mentors(COHORTS_CSV_FILE, MENTORS_CSV_FILE)
    print()
    populate_modules(COURSES_CSV_FILE, MODULES_CSV_FILE)
    print()
    populate_admin_projects(MODULES_CSV_FILE, ADMINS_CSV_FILE, ADMINS_PROJECTS_CSV_FILE)