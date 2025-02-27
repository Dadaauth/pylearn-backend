# """
# Populate your database
# """
# from datetime import date, timedelta
# import csv
# import random
# from faker import Faker

# from app.models.project import CohortProject

# fake = Faker()


# def populate_cohort_projects(cohorts_csv_file, admin_projects_csv_file, cohort_projects_csv_file):
#     cohorts = generate_fake_data(cohorts_csv_file, admin_projects_csv_file)
#     print(f"Fake CohortProject data successfully generated")

#     db_data = save_cohort_projects_to_db(cohorts)
#     print(f"Fake CohortProject data successfully saved to database")

#     save_data_to_csv(cohort_projects_csv_file, db_data)
#     print(f"Fake CohortProject data successfully generated and saved to {cohort_projects_csv_file}")

# def generate_fake_data(cohorts_csv_file, admin_projects_csv_file):
#     cohorts = []
#     with open(cohorts_csv_file, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             cohorts.append(row)

#     cohorts_with_projects = []
#     for cohort in cohorts:
#         if cohort["status"] == "pending": continue

#         potential_projects = generate_fake_data_for_cohort(admin_projects_csv_file, cohort)
#         if cohort["status"] == "completed":
#             for pproject in potential_projects:
#                 pproject["status"] = "completed"
#         elif cohort["status"] == "in-progress":
#             potential_projects[0]["status"] = "completed"
#             potential_projects[1]["status"] = "second-attempt"
#             potential_projects[2]["status"] = "released"

#         cohorts_with_projects.append({
#             "cohort": cohort,
#             "projects": potential_projects
#         })
#     return cohorts_with_projects

# def generate_fake_data_for_cohort(admin_projects_csv_file, cohort):
#     admin_projects = []
#     with open(admin_projects_csv_file, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             admin_projects.append(row)

#     potential_projects = []
#     for admin_project in admin_projects:
#         if admin_project['course_id'] == cohort["course_id"]:
#             potential_projects.append(admin_project)

#     if cohort["status"] == "in-progress":
#         tmp = []
#         for i in range(3):
#             tmp.append(potential_projects[i])
#         potential_projects = tmp
#     return potential_projects

# def create_project_in_db(project_dict, cohort):
#     # Add attributes needed by CohortProject
#     project_dict["project_pool_id"] = project_dict["id"]
#     project_dict['fa_start_date'] = date.today()
#     project_dict['sa_start_date'] = date.today() + timedelta(days=int(project_dict["fa_duration"]))
#     project_dict['end_date'] = project_dict['sa_start_date'] + timedelta(days=int(project_dict["sa_duration"]))
#     project_dict['cohort_id'] = cohort["id"]
#     project_dict['prev_project_id'] = None
#     project_dict['next_project_id'] = None
    
#     # Remove attributes not needed by CohortProject
#     del project_dict["id"]
#     del project_dict["fa_duration"]
#     del project_dict["sa_duration"]
#     del project_dict["release_range"]
    
#     last_project = CohortProject.search(cohort_id=cohort["id"], next_project_id=None)
#     # Create a new CohortProject instance
#     new_project = CohortProject(**project_dict)
#     new_project.save()
#     new_project.refresh()
#     data = [new_project.id]
#     data.extend(project_dict.values())
#     if last_project:
#         last_project.update(next_project_id=new_project.id)
#         new_project.update(prev_project_id=last_project.id)
#         last_project.save()
#         new_project.save()
#     return data

# def save_projects_for_cohort(cohort):
#     projects = cohort["projects"]
#     cohort = cohort["cohort"]
#     csv_data_s = []
#     for project in projects:
#         data = create_project_in_db(project, cohort)
#         csv_data_s.append(data)
#     return csv_data_s

# def save_cohort_projects_to_db(cohorts):
#     db_data = []
#     for cohort in cohorts:
#         db_data.extend(save_projects_for_cohort(cohort))
#     return db_data

# def save_data_to_csv(filename, data):
#     with open(filename, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)

#         # Write header
#         writer.writerow(["id", "title", "module_id", "author_id",
#                         "course_id", "status", 
#                         "next_project_id", 'prev_project_id',
#                         "project_pool_id", "fa_start_date", "sa_start_date",
#                         "end_date", "cohort_id"])
#         for dt in data:
#             # dt must be a list
#             writer.writerow(dt)
