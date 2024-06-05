# Todo List Application

This is a simple Todo List application built using Flask, SQLite, and Flask-Login for user authentication. The application allows users to register, log in, and manage their own tasks. Users can add, edit, delete, and filter tasks based on various criteria.

## Features

- User authentication (register, login, logout)
- Add, edit, and delete tasks
- Filter tasks based on status (done/not done), priority, and search keywords
- Tasks are associated with individual users
- Inline task editing
- Tasks have a priority level and due date
- Prevent selecting past dates for task due dates

## Requirements

- Python 3.x
- Flask
- Flask-Login
- SQLite
- Werkzeug (for password hashing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/647825/The-Selection-Lab.git
   cd The-Selection-Lab
   cd todo-list-app
   ```

2. Install the required packages:

   ```bash
   pip install Flask Flask-Login
   ```

3. Initialize the database:

   ```python
   python -c "import models; models.init_db(); models.update_db()"
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`.

## Usage

### Register

1. Go to the register page by clicking the "Register here" link on the login page.
2. Enter a unique username and password.
3. Click the "Register" button.

### Login

1. Enter your username and password on the login page.
2. Click the "Login" button.

### Add a Task

1. After logging in, fill out the form at the bottom of the main page to add a task.
2. Enter the task title, description, priority, and due date.
3. Click the "Add Task" button.

### Edit a Task

1. Click the "Edit" link next to the task you want to edit.
2. Update the task details in the form that appears.
3. Click the "Update Task" button.

### Delete a Task

1. Click the "Delete" link next to the task you want to delete.

### Filter Tasks

1. Use the search bar and dropdown filters at the top of the main page to filter tasks based on status, priority, and keywords.

### Logout

1. Click the "Logout" button in the top right corner of the page.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [SQLite](https://www.sqlite.org/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)
