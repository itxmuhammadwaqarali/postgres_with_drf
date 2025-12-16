DRF Users — README

**Project**: DRF Users (Django + Django REST Framework)

**Overview**: This small project provides user management with JWT authentication (access + refresh tokens) using PostgreSQL as the database. It also includes API documentation via `drf-spectacular` (Swagger / ReDoc).

**Prerequisites**:
- Python 3.11+ (project uses Python 3.12 in the virtualenv here)
- PostgreSQL running and accessible
- A virtual environment (recommended)

**Environment**:
- The project reads configuration from environment variables. A `.env` file in the repository root is supported for local development (loaded by `python-dotenv` when installed).
- Keys used by the app:
  - `SECRET_KEY` — Django secret key (required when `DEBUG=False`)
  - `DJANGO_DEBUG` — set to `1`/`true` to enable debug mode locally
  - `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — database settings

**Local setup (recommended)**

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
# If requirements.txt is not present, at minimum install:
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular python-dotenv psycopg2-binary
```

3. Create a `.env` file at the project root (or export environment variables). Example `.env`:

```env
DJANGO_DEBUG=True
SECRET_KEY=changeme-for-dev-only
DB_ENGINE=django.db.backends.postgresql
DB_NAME= ---
DB_USER=----
DB_PASSWORD=---
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations and create a superuser:

```bash
cd core
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Documentation & API endpoints
- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`
- Raw OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

Auth endpoints (example)
- Login: `POST /api/users/login/` with JSON `{"username": "<user>", "password": "<pass>"}` — returns `access`, `refresh`, and `user` info.
- Logout: `POST /api/users/logout/` with header `Authorization: Bearer <access_token>` and JSON `{"refresh": "<refresh_token>"}` — blacklists refresh tokens.
- Create user: `POST /api/users/create/` (requires admin role and authentication as currently implemented)
