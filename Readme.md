# Project Management Tool

A Django-based REST API for managing projects, tasks, and comments, with features like user registration, authentication, and project collaboration.

---

## 1. Project Title and Description

**Project Name**: Project Management Tool

**Description**: A Django-based REST API for managing projects, tasks, and comments, with features like user registration, authentication, and project collaboration.

---

## 2. Features

1. User Registration and Login with Token-based Authentication.
2. Project Management (Create, Read, Update, Delete).
3. Task Management with status and priority tracking.
4. Comments on tasks for collaboration.
5. Role-based access to projects.

---

## 3. Technologies Used

1. **Backend**: Django, Django REST Framework (DRF)
2. **Authentication**: Token-based Authentication (DRF)
3. **API Documentation**: DRF-YASG or DRF-Spectacular
4. **Database**: SQLite (default for development)

---

## 4. Prerequisites

1. Python 3.10 or higher.
2. Pip (Python package manager).
3. Virtual Environment (optional but recommended).

---

## 5. Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/a-bibash/APIprojectmangement
   cd project_management
   ```

2. **Create and Activate a Virtual Environment**:

   - On Linux/Mac:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin Account)**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django Development Server**:

   ```bash
   python manage.py runserver
   ```

   The web application will be available at `http://127.0.0.1:8000/`.

---

## 6. API Endpoints

### User Authentication

1. **Register**: `POST /api/users/register/`
2. **Login**: `POST /api/users/login/`

### Projects

1. **List/Create Projects**: `GET/POST /api/projects/`
2. **Project Details**: `GET/PUT/DELETE /api/projects/{id}/`

### Tasks

1. **List/Create Tasks**: `GET/POST /api/tasks/`
2. **Task Details**: `GET/PUT/DELETE /api/tasks/{id}/`

### Comments

1. **List/Create Comments**: `GET/POST /api/comments/`
2. **Comment Details**: `GET/PUT/DELETE /api/comments/{id}/`

---

## 7. API Documentation

1. **Access Swagger UI**:
   - Run the server.
   - Visit: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 8. Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## 9. License

This project is licensed under the MIT License.

