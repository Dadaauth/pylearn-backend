"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.course import Course

fake = Faker()


def populate_courses(csv_filename):
    data = generate_fake_data()
    print(f"Fake courses data successfully generated")
    
    db_data = save_courses_to_db(data)
    print(f"Fake courses data successfully saved to database")

    save_data_to_csv(csv_filename, db_data)
    print(f"Fake courses data successfully generated and saved to {csv_filename}")



def generate_fake_data():
    fake_data = [
        {
            "title": "Software Engineering",
            "status": "published",
            "communication_channel": "https://discord/invite",
        },
        {
            "title": "UI/UX Design",
            "status": "published",
            "communication_channel": "https://discord/invite",
        },
        {
            "title": "Video Editing",
            "status": "published",
            "communication_channel": "https://discord/invite",
        }
    ]
    return fake_data

def save_courses_to_db(data):
    db_data = []
    for row in data:
        course = Course(**row)
        data = [course.id]
        data.extend(list(row.values()))
        db_data.append(data)
        course.save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "title", "status", "communication_channel"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
