# Django Architecture & Project Structure Guide

This document outlines the recommended architecture and project structure for the **Kishkinda University Platform** backend, built with Django.

## 1. Django App Structure (`backend/apps/`)

To keep the project modular and scalable, all domain-specific Django apps should be placed inside the `backend/apps/` directory.

### Recommended Apps:
- **`accounts/`**: Custom user models, authentication, and role-based access control (RBAC).
- **`dashboard/`**: Aggregated views, metrics, and home screens for different user roles.
- **`universities/`**: Top-level entity management (University details, global settings).
- **`colleges/`**: College management within the university.
- **`departments/`**: Departmental structures and hierarchies within colleges.
- **`students/`**: Student profiles, enrollment history, and personal details.
- **`faculty/`**: Faculty profiles, designations, and workload.
- **`academics/`**: Courses, programs, syllabus, and academic calendars.
- **`attendance/`**: Student and faculty attendance tracking.
- **`exams/`**: Exam schedules, halls, grading, and result generation.
- **`finance/`**: Fee management, payroll, and transactions.
- **`notices/`**: Announcements, circulars, and messaging systems.
- **`documents/`**: Document storage, certificates, and verification systems.

### Internal App Structure:
Each app should follow a standard internal structure:
```text
backend/apps/<app_name>/
    __init__.py
    admin.py
    apps.py
    models.py
    urls.py
    views.py
    serializers.py  # If using Django REST Framework
    services.py     # Business logic separated from views
    selectors.py    # Complex database queries separated from views
    tests/          # Directory for tests instead of a single tests.py
```

## 2. Template Organization (`backend/templates/`)

For server-rendered pages and emails, templates should be organized globally rather than inside individual apps to make them easier to locate, override, and maintain.

```text
backend/templates/
    base.html                     # Main layout wrapper
    components/                   # Reusable UI components (navbar, sidebar, etc.)
        navbar.html
        footer.html
    includes/                     # Snippets and partials
        messages.html
    accounts/                     # App-specific templates
        login.html
        profile.html
    dashboard/
        student_dashboard.html
        faculty_dashboard.html
    emails/                       # Email templates (HTML/TXT)
        welcome.html
```

## 3. Static File Organization (`backend/static/`)

Static assets (CSS, JS, images, fonts) should be organized globally. When running `collectstatic`, everything will be gathered here.

```text
backend/static/
    css/
        main.css
        vendors/                  # Third-party CSS libraries
    js/
        main.js
        modules/                  # Page-specific JS files
    images/
        logos/
        avatars/
        placeholders/
    fonts/                        # Custom web fonts
    vendors/                      # Third-party libraries (Bootstrap, Tailwind, etc.)
```

## 4. Django Settings Structure (`backend/config/settings/`)

A single `settings.py` file becomes unmanageable as the project grows. A module approach separating base, local, and production settings is recommended.

```text
backend/config/settings/
    __init__.py
    base.py         # Common settings for all environments
    local.py        # Development-only settings (DEBUG=True, SQLite/Local DB)
    production.py   # Production settings (DEBUG=False, Security, Cache, Logging)
    test.py         # Settings specifically for CI and running tests
```

### Key Practices:
- **`base.py`**: Load environment variables here (using `python-dotenv` or `environ`).
- **`local.py`**: Import `base.py` and override settings like `DATABASES`, `ALLOWED_HOSTS`, and cross-origin resource sharing (CORS).
- **`production.py`**: Enforce strict security settings (`SECURE_SSL_REDIRECT`, `CSRF_COOKIE_SECURE`), set up real email backends, and configure caching (Redis/Memcached).

## 5. Recommended Overall Scalable Structure

Here is the complete holistic view of the recommended backend structure designed for scalability and maintainability:

```text
kishkinda-university-platform/
├── backend/
│   ├── apps/                    # All domain logic
│   │   ├── accounts/
│   │   ├── academics/
│   │   ├── ... (other apps)
│   ├── config/                  # Core Django configuration
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── production.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── urls.py              # Main URL routing
│   ├── templates/               # Global HTML templates
│   ├── static/                  # Global static assets
│   ├── media/                   # User-uploaded files
│   ├── manage.py
│   ├── requirements.txt         # Or Pipfile/pyproject.toml
│   └── .env                     # Environment variables (IGNORED IN GIT)
├── frontend/                    # Separate frontend app (React/Vue/Next.js)
├── docs/                        # Project documentation
│   └── architecture/
│       └── day1-django-architecture.md
└── screenshots/                 # UI/UX References
```

### Future-Proofing Recommendations:
- **Fat Models, Thin Views**: Keep views clean by pushing logic to models, or better yet, a `services.py` layer.
- **API First**: If a frontend framework is planned, expose functionality using Django REST Framework (DRF) or Django Ninja. Put `serializers.py` in each app.
- **Environment Variables**: Never hardcode secrets. Use `.env` extensively.
- **Task Queues**: Plan for background tasks (Celery/Redis) early, especially for sending notifications or report generation.
