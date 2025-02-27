"""
Populate your database
"""
import csv
import random
from faker import Faker

from app.models.project import AdminProject

fake = Faker()


def populate_admin_projects(modules_csv_file, admins_csv_file, admin_projects_csv_file):
    courses = generate_fake_data(modules_csv_file, admins_csv_file)
    print(f"Fake AdminProject data successfully generated")

    db_data = save_admin_projects_to_db(courses)
    print(f"Fake AdminProject data successfully saved to database")

    save_data_to_csv(admin_projects_csv_file, db_data)
    print(f"Fake AdminProject data successfully generated and saved to {admin_projects_csv_file}")


def generate_projects_for_module(module, admins):
    dt = [
            {
                "title": "Project 1",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 2",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 3",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 4",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 5",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 6",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 7",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 8",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 9",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 10",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
            {
                "title": "Project 11",
                "module_id": module["id"],
                "author_id": random.choice(admins)["id"],
                "course_id": module["course_id"],
                "status": "published",
                "fa_duration": random.randint(1, 5),
                "sa_duration": random.randint(1, 10),
                "release_range": random.randint(0, 6),
                "next_project_id": None,
                "prev_project_id": None,
            },
        ]
    return dt

def generate_fake_data(modules_csv_file, admins_csv_file):
    modules = []
    admins = []
    with open(modules_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            modules.append(row)
    with open(admins_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            admins.append(row)

    current = {
        "course_id": modules[0]["course_id"],
        "index": 0,
        "modules": []
    }
    courses = [current]
    for module in modules:
        if module["course_id"] == current["course_id"]:
           current["modules"].append(module)
        else:
            current = {
                "course_id": module["course_id"],
                "index": current["index"] + 1,
                "modules": []
            }
            courses.append(current)

    for course in courses:
        for module in course["modules"]:
            module["projects"] = generate_projects_for_module(module, admins)

    return courses

def save_admin_project_for_course(course):
    db_data = []
    prev_pid = None
    for module in course["modules"]:
        for row in module["projects"]:
                row["prev_project_id"] = prev_pid
                project = AdminProject(**row)
                project_id = project.id
                project.save()
                project.refresh()
                data = [project_id]
                data.extend(list(row.values()))
                db_data.append(data)
                if prev_pid:
                    prev_project = AdminProject.search(id=prev_pid)
                    prev_project.update(next_project_id=project_id)
                    prev_project.save()
                prev_pid = project_id
    return db_data

def save_admin_projects_to_db(courses):
    db_data = []
    for course in courses:
        db_data.extend(save_admin_project_for_course(course))
    return db_data

def save_data_to_csv(filename, data):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["id", "title", "module_id", "author_id", "course_id", "status", 
                        "fa_duration", "sa_duration", "release_range", "next_project_id",
                        "prev_project_id"])

        for dt in data:
            # dt must be a list
            writer.writerow(dt)
