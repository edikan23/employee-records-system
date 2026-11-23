# Employee Records Management System

A web application that lets TechSolutions Inc. manage employee records in one place instead of scattered spreadsheets.

## Features
- User authentication (sign up, sign in, sign out)
- Role-based access control: **Admin**, **HR Manager**, **Employee**
- Employee registration, editing and deletion
- Search by name, email, employee ID or job title, with department and status filters
- Employee account linking (an HR manager links a login account to an employee record)
- Dashboard with headcount and department breakdown
- Django admin dashboard at `/admin/`

## Roles
| Role | Can do |
|------|--------|
| Admin (superuser) | Everything, including the admin dashboard and user/group management |
| HR Manager (group) | Register, edit, delete, search and link accounts to employees |
| Employee | View only their own linked employee record |

To make someone an HR Manager: open `/admin/`, edit the user, and add them to the **HR Manager** group.

## Technologies
- Backend: Python, Django
- Frontend: HTML5, CSS3, JavaScript
- Database: SQLite (local development), MySQL (production)
- Deployment: GitHub, Heroku (Gunicorn, WhiteNoise)

## How to Run Locally
```bash
git clone https://github.com/YOUR-USERNAME/employee-records-system.git
cd employee-records-system
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo     # optional demo users and employees
python manage.py runserver
```
Open http://127.0.0.1:8000/employees/

Demo logins (local only, from `seed_demo`): `admin / Admin12345!`, `hr_manager / HrManager123!`, `ada / Employee123!`

Run the tests with `python manage.py test`.

## Deploy to Heroku
```bash
heroku create your-app-name
heroku addons:create jawsdb:kitefin          # MySQL; sets JAWSDB_URL
heroku config:set DEBUG=False SECRET_KEY="long-random-string" ALLOWED_HOSTS=your-app-name.herokuapp.com
git push heroku main                          # runs migrations via the Procfile release phase
heroku run python manage.py createsuperuser
```
Static files are collected automatically during the Heroku build and served by WhiteNoise.

## Project Structure
```
manage.py
employee_records_system/   settings, root URLs, WSGI
employees/                 models, views, forms, roles (RBAC), templates, static files, tests
Procfile                   Heroku process and release commands
requirements.txt           dependencies
```

## Current Status
Foundation and core features are in place. Further modules can extend reporting, departments management and audit history.

## Module 2 Notes

### Servers
- `python manage.py runserver`: Django's development server. It reloads when code changes and is meant for development and testing only.
- `gunicorn employee_records_system.wsgi:application`: a production-style application server. It does not reload on changes and is the server used on Heroku.

### Debugging with Browser DevTools
- Used the Elements panel to inspect the page and made a temporary heading change that reset on refresh.
- Checked the Console and Network panels for errors and requests.
- Found that the site had no favicon, so the browser requested `/favicon.ico`. Added a `<link rel="icon">` to `base.html` to fix it.

### Frontend enhancement
- Added a "Show quick guide" button on the home page that shows and hides a short guide box using HTML, CSS and JavaScript.

## Open-Source Component Evaluation

**Component Name:** django-import-export

**Purpose:** A Django library for importing and exporting data in formats such as CSV and Excel, with support in the Django admin.

**Potential Use:** TechSolutions currently keeps employee data in spreadsheets. This library could let HR upload those spreadsheets to create employee records in bulk and export employee lists for reporting, instead of retyping records.

**Decision:** Test later. It is not added to this project now. Before adopting it, check that it supports the project's Django version and review its documentation and maintenance status.