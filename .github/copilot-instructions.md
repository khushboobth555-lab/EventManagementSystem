# 🧑‍💻 Copilot Instructions for Event Management System (EMS)

## Project Overview
- **Framework:** Django (Python)
- **Main App:** `event/` (handles events, users, forms, templates)
- **Settings:** `EMS/` (project config, URLs, WSGI)
- **Static/Media:** `static/` for assets, `media/` for uploads
- **Database:** SQLite by default (`db.sqlite3`), can be swapped for PostgreSQL/MySQL

## Key Workflows
- **Setup:**
  - Create and activate a Python virtual environment
  - Install dependencies: `pip install -r requirements.txt`
  - Apply migrations: `python manage.py migrate`
  - Create admin: `python manage.py createsuperuser`
  - Run server: `python manage.py runserver`
- **Testing:**
  - Run tests: `python manage.py test event`
- **Static/Media:**
  - Static files in `static/`, media uploads in `media/`
  - Use Django's `collectstatic` for deployment

## Architecture & Patterns
- **Apps:**
  - `event/` is the core app. Models, views, forms, and admin customizations live here.
  - Templates are organized under `event/templates/event/`.
  - Custom template tags: `event/templatetags/form_tags.py`
- **URLs:**
  - Project-level: `EMS/urls.py`
  - App-level: `event/urls.py`
- **Forms:**
  - Custom forms in `event/forms.py` (use Django forms for validation/UI)
- **Admin:**
  - Custom admin logic in `event/admin.py`
- **Migrations:**
  - All migrations in `event/migrations/`

## Conventions & Tips
- **Template Inheritance:**
  - Use `base.html` in `event/templates/event/` for layout inheritance
- **Error Pages:**
  - Custom error templates: `event/templates/400.html`, `403.html`, etc.
- **Static/Media Paths:**
  - Reference static files with `{% static 'event/css/style.css' %}`
  - Reference media files via Django's media settings
- **Testing:**
  - Place tests in `event/tests.py`
- **Admin:**
  - Register models in `event/admin.py`

## External Dependencies
- **Bootstrap** for frontend styling
- **Django** (see `requirements.txt` for all packages)

## Examples
- **Add a new event model:** Edit `event/models.py`, run `makemigrations` and `migrate`
- **Add a template:** Place HTML in `event/templates/event/`, update views in `event/views.py`
- **Add a static asset:** Place in `static/event/css/` or `static/event/js/`

---

For more details, see `README.md` and explore the `event/` app for core logic.

---

*Update this file if project structure or conventions change.*
