# Healthcare Backend

A small Django REST API for user accounts, patients, doctors, and patient-doctor assignments.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create a PostgreSQL database and set the variables listed in `.env.example` in your environment. For example, in PowerShell, set `$env:SECRET_KEY` and `$env:DB_PASSWORD` before running the server. The example file documents the variables; Django does not load it automatically.
4. Run `python manage.py migrate`.
5. Start the server with `python manage.py runserver`.

## Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `GET`, `POST`, `GET /<id>/`, `PUT /<id>/`, `PATCH /<id>/`, `DELETE /<id>/` at `/api/patients/`
- The same CRUD methods at `/api/doctors/`
- `GET`, `POST /api/mappings/`
- `GET /api/mappings/<patient_id>/`
- `DELETE /api/mappings/<mapping_id>/`

Send the JWT access token in the `Authorization: Bearer <token>` header for protected endpoints. Patient and mapping data is limited to the authenticated user's patients. Doctors are shared across users.
