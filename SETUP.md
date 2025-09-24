# Event Management System Setup Instructions

This guide will help you set up and run the Event Management System Django application.

## Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Installation Steps

1. **Clone the Repository**
   ```sh
   git clone <your-repo-url>
   cd EMS
   ```

2. **Create a Virtual Environment (Recommended)**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin Account)**
   ```sh
   python manage.py createsuperuser --username=test --email=test@gmail.com
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```
   Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Notes
- Static and media files are served automatically in development.
- If you see a warning about URL namespaces, ensure you do not have duplicate `app_name` values in your Django apps.
- For any issues, check the terminal output for error messages and follow the instructions.

## Project Structure
- `EMS/` - Main Django project settings
- `event/` - Event management app
- `user/` - User management app
- `media/` - Uploaded files
- `static/` - Static files (CSS, JS, images)

## Troubleshooting
- If you encounter migration errors, delete the `db.sqlite3` file and all migration files except `__init__.py`, then re-run migrations.
- For import errors, ensure models and forms are imported from the correct app (e.g., `Profile` from `user.models`).
