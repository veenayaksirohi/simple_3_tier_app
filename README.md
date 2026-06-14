# Simple 3-Tier Application

A beginner-friendly 3-tier app:

- **Frontend**: HTML + JavaScript
- **Backend**: Python Flask API
- **Database**: PostgreSQL

## What it does
You can add todo items and list them from the database.

## Run with Docker Compose

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- Backend health: http://localhost:5000/health
- API: http://localhost:5000/todos

## Project structure

- `frontend/` = simple web page
- `backend/` = Flask API
- `db/` = PostgreSQL initialization script
- `docker-compose.yml` = runs all 3 tiers

## API

### GET /health
Returns backend status.

### GET /todos
Returns all todo items.

### POST /todos
Add a todo item.

Example JSON:
```json
{
  "title": "Learn Docker"
}
```
