# Todos

A simple Todo list REST API built with Django and Django REST Framework. Each user registers, logs in to get an auth token, and then manages their own private list of todos.

## Features

- User registration and login with token-based authentication (`rest_framework.authtoken`)
- Logout (deletes the auth token)
- Create, list, retrieve, update, and delete todos
- Todos are scoped per user — you can only see and manage your own
- SQLite database (zero config for local development)

## Tech Stack

- Python
- Django 6.1
- Django REST Framework 3.18
- python-dotenv (for environment variable management)
- SQLite (default database)

## Project Structure

```
todos/
├── todos/            # Project settings, root URLs, WSGI/ASGI
├── api/               # Todo model, views, serializers, and routes
├── user_auth/          # Registration, login, logout
├── manage.py
├── requirements.txt
└── .env.example
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd todos
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create a superuser for the admin site

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Authentication

This API uses DRF's `TokenAuthentication`. After logging in, include the returned token in the `Authorization` header for all protected endpoints:

```
Authorization: Token <your-token>
```

All `api/` endpoints (todos) require authentication. The `register` and `login` endpoints are open to everyone.

## API Endpoints

### Auth (`user_auth`)

| Method | Endpoint         | Description                          | Auth required |
|--------|------------------|---------------------------------------|----------------|
| POST   | `/register/`     | Create a new user account             | No             |
| POST   | `/login/`        | Log in and receive an auth token      | No             |
| POST   | `/logout/`       | Log out (deletes the current token)   | Yes            |

**Register**

```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "jane", "password": "supersecret"}'
```

**Login**

```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "jane", "password": "supersecret"}'
```

Response:

```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4" }
```

**Logout**

```bash
curl -X POST http://127.0.0.1:8000/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4"
```

### Todos (`api`)

| Method | Endpoint         | Description                       | Auth required |
|--------|------------------|-------------------------------------|----------------|
| GET    | `/`              | API root — links to `todos`         | Yes            |
| GET    | `/todos/`        | List the current user's todos       | Yes            |
| POST   | `/todos/`        | Create a new todo                    | Yes            |
| GET    | `/todo/<id>/`    | Retrieve a single todo               | Yes            |
| PUT    | `/todo/<id>/`    | Update a todo (full update)          | Yes            |
| PATCH  | `/todo/<id>/`    | Update a todo (partial update)       | Yes            |
| DELETE | `/todo/<id>/`    | Delete a todo                        | Yes            |

**Create a todo**

```bash
curl -X POST http://127.0.0.1:8000/todos/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false}'
```

**List todos**

```bash
curl http://127.0.0.1:8000/todos/ \
  -H "Authorization: Token <your-token>"
```

**Update a todo**

```bash
curl -X PATCH http://127.0.0.1:8000/todo/1/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Delete a todo**

```bash
curl -X DELETE http://127.0.0.1:8000/todo/1/ \
  -H "Authorization: Token <your-token>"
```

## Todo Model

| Field         | Type        | Notes                          |
|---------------|-------------|----------------------------------|
| `title`       | CharField    | Max length 100                  |
| `description` | TextField    |                                  |
| `completed`   | BooleanField | Defaults to `False`              |
| `created_at`  | DateTimeField| Auto-set on creation, read-only |
| `user`        | ForeignKey   | Owner of the todo (set automatically from the logged-in user) |

## Admin Site

Django's built-in admin is available at `/admin/`. Log in with a superuser account to view and manage todos directly.

## Notes / Known Limitations

- `DEBUG` defaults to `True` and `ALLOWED_HOSTS` defaults to an empty list if not set in `.env` — make sure to configure both properly before deploying.
- The login endpoint returns `{"error": "Invalid username or password!"}` with a `200 OK` status rather than a `401`; adjust as needed if you plan to consume this from a strict client.
- No password confirmation or strength validation is enforced beyond Django's default `AUTH_PASSWORD_VALIDATORS` on the `register` endpoint.

## License

Add your license of choice here.