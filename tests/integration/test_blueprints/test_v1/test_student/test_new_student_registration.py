"""
Test cases for /api/v1/student/project/<project_id>/submit POST endpoint
Test Cases:
    - required attributes not present
    - student already exists
    - sent course_id does not exist for any course
    - success:
        - status code 201
        - record must be persisted in the database
        - student account status should be set to inactive
    - no cohort_id sent
        - cohort assigned to student should be the last cohort in the list
"""