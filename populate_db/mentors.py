"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.user import Mentor, MentorCohort

fake = Faker()


def populate_mentors(cohorts_csv_file, mentors_csv_file):
    data = generate_fake_data()
    print(f"Fake Mentors user data successfully generated")
    
    db_data = save_mentors_to_db(data, cohorts_csv_file)
    print(f"Fake Mentors user data successfully saved to database")

    save_data_to_csv(mentors_csv_file, db_data)
    print(f"Fake Mentors user data successfully generated and saved to {mentors_csv_file}")



def generate_fake_data():
    fake_data = []
    for _ in range(30):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        password = fake.password()
        username = str(uuid4())
        phone = fake.phone_number()
        status = random.choice(["active", "inactive", "suspended", "deleted"])
        fake_data.append({
            "first_name": first_name, "last_name": last_name,
            "email": email, "password": password,
            "username": username, "phone": phone,
            "status": status
        })
    return fake_data

def save_mentors_to_db(data, cohorts_csv_file):
    cohorts_tmp = []
    with open(cohorts_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cohorts_tmp.append(row)

    db_data = []
    for row in data:
        cohorts = random.sample(cohorts_tmp, random.randint(2, 5))
        mentor = Mentor(**row)
        mentor_id = mentor.id
        data = [mentor_id]
        data.extend(list(row.values()))
        db_data.append(data)
        mentor.save()
        # Assign mentors to all cohorts
        for cohort in cohorts:
            MentorCohort(mentor_id=mentor_id, cohort_id=cohort["id"]).save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "first_name", "last_name", "email", "password", "username", "phone", "status"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
