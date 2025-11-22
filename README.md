# Website Builder AI — Full-Stack AI-Powered Website Generator

## Milestone 1 — Secure User Authentication (COMPLETE)

### Tech Stack
- FastAPI (Python) — Backend
- PostgreSQL + SQLAlchemy (Async)
- React + Tailwind CSS (coming next)
- JWT Authentication (next step)
- Docker + GitHub Actions + AWS (future)

### Features Already Working
- User signup with email + password
- Secure bcrypt password hashing
- Real PostgreSQL database (async)
- Clean architecture (models / schemas / crud)
- Swagger UI at `/docs`
- Environment variables
- Production-ready setup from day 1

### Live Demo (Local)
```bash
cd backend
uvicorn main:app --reload
→ http://127.0.0.1:8000/docs