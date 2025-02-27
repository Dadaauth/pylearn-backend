"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.cohort import Cohort

fake = Faker()


def populate_cohorts(courses_csv_file, cohorts_csv_file):
    data = generate_fake_data(courses_csv_file)
    print(f"Fake cohorts data successfully generated")
    
    db_data = save_cohorts_to_db(data)
    print(f"Fake cohorts data successfully saved to database")

    save_data_to_csv(cohorts_csv_file, db_data)
    print(f"Fake cohorts data successfully generated and saved to {cohorts_csv_file}")



def generate_fake_data(courses_csv_file):
    courses = []
    with open(courses_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            courses.append(row)

    fake_data = []
    for course in courses:
        dt = [
            {
                "name": "Cohort-1",
                "status": "completed",
                "course_id": course["id"]
            },
            {
                "name": "Cohort-2",
                "status": "completed",
                "course_id": course["id"]
            },
            {
                "name": "Cohort-3",
                "status": "in-progress",
                "course_id": course["id"]
            },
            {
                "name": "Cohort-4",
                "status": "in-progress",
                "course_id": course["id"]
            },
            {
                "name": "Cohort-5",
                "status": "pending",
                "course_id": course["id"]
            },
        ]
        fake_data.extend(dt)
    return fake_data

def save_cohorts_to_db(data):
    db_data = []
    for row in data:
        course = Cohort(**row)
        data = [course.id]
        data.extend(list(row.values()))
        db_data.append(data)
        course.save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "name", "status", "course_id"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
