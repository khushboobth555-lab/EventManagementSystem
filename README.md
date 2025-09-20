# 🎉 Event Management System (EMS)

A web-based Event Management System built with **Django**.  
This project allows users to manage, create, and track events effectively.

---

## 🚀 Features
- User authentication (login, register, logout)
- Event creation, update, delete
- Event registration for users
- Admin dashboard for event management
- Media and static file handling

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Others:** Django Admin, Static & Media files

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/khushboobth555-lab/EventManagementSystem.git
cd EventManagementSystem

2. Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate

5. Create a superuser (for admin access)
python manage.py createsuperuser

6. Run the development server
python manage.py runserver


Visit 👉 http://127.0.0.1:8000/
 in your browser.

📂 Project Structure
EventManagementSystem/
│── EMS/               # Project settings
│── event/             # Main app (events handling)
│── media/             # Uploaded media files
│── static/            # Static assets (CSS, JS, images)
│── manage.py          # Django project manager
│── requirements.txt   # Python dependencies
│── db.sqlite3         # SQLite database (not recommended to commit)


👩‍💻 Author

Developed by Khushboo 💻
GitHub: khushboobth555-lab