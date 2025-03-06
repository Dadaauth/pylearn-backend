# Testing

## What to test

### Unit Tests

* Models and Database Operations
  * Check if models correctly store and retrieve data.
  * Ensure relationships and constraints work as expected.
* Utility Functions
  * Test custom helper functions (e.g., date formatting, hashing).

### Route & API Tests (Testing Endpoints)

* Response Status Codes
  * Test if routes return 200 OK, 201 Created, 400 Bad Request, etc.
* Authentication & Authorization
  * Ensure that protected routes require authentication
  * Test login/logout functionality
* Request Payloads & Responses
  * Check if the API correctly handles valid/invalid JSON

### Form Validation & Input Handling

* Check Required Fields
  * Ensure missing fields return proper errors.

### Database Testing

* Data Persistence
  * Ensure data is saved and retrieved correctly
* Transactions & Rollbacks
  * Test if failures properly rollback transactions

### Performance & Load Testing

* Check if the app can handle multiple requests without slowing down
* Use Locust or JMeter for load testing

### Security Tests

* Authentication bypass attempts
* CSRF & XSS protection
* Data exposure in API responses

### Integration Tests

* Test interactions between components like database, API, authentication, and external services.

## 🛠️ Tools for Flask Testing

* pytest – for running unit tests (pip install pytest)
* Flask-Testing – testing helpers for Flask apps
* unittest – built-in Python testing framework
* requests – for API testing
* Locust / JMeter – for load testing
