"""
Populate your database with new test admin users
"""
import csv
from uuid import uuid4
import random
from faker import Faker

from app.models.user import Admin

fake = Faker()


def populate_admins(csv_filename):
    data = generate_fake_data()
    print(f"Fake Admins user data successfully generated")
    
    db_data = save_admins_to_db(data)
    print(f"Fake Admins user data successfully saved to database")

    save_data_to_csv(csv_filename, db_data)
    print(f"Fake Admins user data successfully generated and saved to {csv_filename}")



def generate_fake_data():
    fake_data = []
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        password = fake.password()
        username = uuid4()
        phone = fake.phone_number()
        status = random.choice(["active", "inactive", "suspended", "deleted"])
        fake_data.append({
            "first_name": first_name, "last_name": last_name,
            "email": email, "password": password,
            "username": username, "phone": phone,
            "status": status
        })
    return fake_data

def save_admins_to_db(data):
    db_data = []
    for row in data:
        admin = Admin(**row)
        data = [admin.id]
        data.extend(list(row.values()))
        db_data.append(data)
        admin.save()
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "first_name", "last_name", "email", "password", "username", "phone", "status"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
