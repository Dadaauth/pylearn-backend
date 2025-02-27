"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.user import Student

fake = Faker()


def populate_students(cohorts_csv_file, students_csv_file):
    data = generate_fake_data(cohorts_csv_file)
    print(f"Fake Students user data successfully generated")
    
    db_data = save_students_to_db(data)
    print(f"Fake Students user data successfully saved to database")

    save_data_to_csv(students_csv_file, db_data)
    print(f"Fake Students user data successfully generated and saved to {students_csv_file}")



def generate_fake_data(cohorts_csv_file):
    cohorts = []
    with open(cohorts_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cohorts.append(row)

    fake_data = []
    for _ in range(300):
        cohort = random.choice(cohorts)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        password = fake.password()
        username = uuid4()
        phone = fake.phone_number()
        status = random.choice(["active", "inactive", "suspended", "deleted"])
        points = random.randint(0, 90)
        course_id = cohort["course_id"]
        cohort_id = cohort["id"]
        fake_data.append({
            "first_name": first_name, "last_name": last_name,
            "email": email, "password": password,
            "username": username, "phone": phone,
            "status": status, "points": points,
            "course_id": course_id, "cohort_id": cohort_id
        })
    return fake_data

def save_students_to_db(data):
    db_data = []
    for row in data:
        student = Student(**row)
        data = [student.id]
        data.extend(list(row.values()))
        db_data.append(data)
        student.save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "first_name", "last_name", "email", "password", "username", "phone", "status", "points", "course_id", "cohort_id"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
