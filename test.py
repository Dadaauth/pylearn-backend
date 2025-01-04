def sort_projects(projects):
        if projects is None or projects == []: return projects
        if not isinstance(projects, list): return projects

        # Retrieve the head of the list
        head = None
        for project in projects:
            if project.prev_project_id is None:
                head = project
                break
        
        # sorting process
        tmp = head
        tmp_list = [head]
        while tmp is not None and tmp.next_project_id is not None:
            for project in projects:
                if project.id == tmp.next_project_id:
                    tmp_list.append(project)
                    tmp = project
                    break

        projects = tmp_list
        return projects

class Project:
     def __init__(self, id, prev_project_id, next_project_id, title):
          self.id = id
          self.prev_project_id = prev_project_id
          self.next_project_id = next_project_id
          self.title = title

projects = [
     Project(5, 4, None, "Five"),
     Project(3, 2, 4, "Three"),
     Project(2, 1, 3, "Two"),
     Project(1, None, 2, "One"),
     Project(4, 3, 5, "Four"),
]

for project in sort_projects(projects):     
    print(project.__dict__)