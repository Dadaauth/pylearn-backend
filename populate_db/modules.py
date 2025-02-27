"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.module import Module

fake = Faker()


def populate_modules(courses_csv_file, modules_csv_file):
    data = generate_fake_data(courses_csv_file)
    print(f"Fake modules data successfully generated")
    
    db_data = save_modules_to_db(data)
    print(f"Fake modules data successfully saved to database")

    save_data_to_csv(modules_csv_file, db_data)
    print(f"Fake modules data successfully generated and saved to {modules_csv_file}")



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
                "title": "Module 1",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 2",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 3",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 4",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 5",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 6",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 7",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 8",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 9",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 10",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 11",
                "status": "published",
                "course_id": course["id"]
            },
            {
                "title": "Module 12",
                "status": "published",
                "course_id": course["id"]
            },
        ]
        fake_data.extend(dt)
    return fake_data

def save_modules_to_db(data):
    db_data = []
    for row in data:
        module = Module(**row)
        data = [module.id]
        data.extend(list(row.values()))
        db_data.append(data)
        module.save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "title", "status", "course_id"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
