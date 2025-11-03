# 📚 Library Management System (LMS)

Full-Stack Web Application – A modern digital library platform for managing physical and digital books.  
Supports patrons (users) and administrators (library staff) with full role-based access control (RBAC).
---
## 🔹 Table of Contents
- [Project Overview](#-project-overview)
- [User Roles & Access](#-user-roles--access)
- [Docker Setup (Recommended)](#-docker-setup-recommended)
- [Getting Started](#-getting-started)
---
## 🔹 Project Overview
The Library Management System (LMS) is a web-based platform that simplifies management of both physical and digital library resources.

### 🎯 Goals
- **Users:** Search, borrow, return books, submit reviews.  
- **Admins:** Manage inventory, users, and assets.  
- **Libraries:** Maintain accurate tracking and reporting for circulation data.
---
## 🔹 User Roles & Access
### 👤 Standard User (Patron)
- Search and browse books  
- Borrow and return books  
- View borrowing history  
- Submit ratings and reviews  

### 🧭 Administrator (Librarian / Staff)
- All standard user permissions  
- Add, update, delete books  
- Manage categories & digital assets  
- View all loans and user activity  
---
## 🔹 Docker Setup
### ✅ Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### ⚙️ Setup Steps
```bash
# Clone the project
git clone <https://github.com/jamil-BS23/Project_LMS.git>
cd LMS

# Copy example environment
cp backend/.env.example backend/.env

# Build and start all services
docker compose up --build

## 🚀 Access URLs

| Service                  | URL                           |
|--------------------------|-------------------------------|
| Frontend                 | http://localhost:5174         |
| Backend (FastAPI Docs)   | http://localhost:8000/docs    |
| PostgreSQL               | localhost:5433                |
| MinIO Console            | http://localhost:9001         |
| PgAdmin                  | http://localhost:8080         |


🪣 Default MinIO Credentials: minioadmin / minioadmin
🗄️ Default PgAdmin Credentials: admin@admin.com / admin123

## 🔹 Getting Started
### ✅ Prerequisites
- Node.js v18+
- npm or yarn
- Python v3.8+
- PostgreSQL

### ⚙️ Backend Setup
```html
<h3>⚙️ Backend Setup</h3>

<pre style="background:#0d1117;color:#fff;padding:10px;border-radius:10px;font-family:monospace;">
+-------------------------------+
| cd backend                    |
| python -m venv .venv          |
| source .venv/bin/activate     |
| pip install -r requirements.txt|
| alembic upgrade head          |
| uvicorn app.main:app --reload |
+-------------------------------+
</pre>

💻 Frontend Setup
+-------------------------------+
| cd frontend                   |
| npm install                   |
| npm run dev                    |
|                               |
| Access URLs:                   |
| Frontend → http://localhost:5173 |
| Backend  → http://localhost:8000/docs |
+-------------------------------+
🔹 Core Features
👥 User Features
   -Search/browse books by title, author, or ISBN
   -Borrow and return books
   -Rate and review titles
   -personal loan history

🛠️ Admin Features
   -Add, edit, delete books and categories
   -Manage user loans and assets
   -Upload and organize digital media (PDFs, covers)

🔹 Technical Stack
  -Frontend	React + Vite + Tailwind CSS + DaisyUI
  -Routing	React Router DOM v6
  -State Management	React Context API
  -HTTP Client	Axios
  -Backend	FastAPI
  -ORM	SQLAlchemy (Async)
  -Database	PostgreSQL
  -File Storage	MinIO
  -Authentication	JWT, RBAC
🔹 Routing & State Management
  -Role-based route protection
  -AuthProvider manages login state
  -Layout shells for each role (Admin/User)

🔹 API Endpoints
📦 Authentication & User Interaction

+----------------+--------+------------------------+---------------+---------------------------+
| Endpoint       | Method | Body / Query           | Response      | Notes                     |
+----------------+--------+------------------------+---------------+---------------------------+
| auth/register  | POST   | email, password        | 201 Created   | 409 if email exists       |
| auth/login     | POST   | email, password        | 200 OK (JWT)  | 401 Unauthorized          |
| books/rate/{id}| POST   | rating, review_text    | 201 Created   | 400 if already rated      |
+----------------+--------+------------------------+---------------+---------------------------+

📦 Catalog & Borrowing

+------------------+--------+-----------------------------------+
| Endpoint         | Method | Notes                             |
+------------------+--------+-----------------------------------+
| books            | GET    | Query: category, search, pagination|
| books/{id}       | GET    | Detailed book info                 |
| books/borrow/{id}| POST   | Borrow a book (auth only)          |
| books/return/{id}| POST   | Return a book (auth only)          |
+------------------+--------+-----------------------------------+

📦 Admin Operations

+-------------------+--------+--------------------------------------+
| Endpoint          | Method | Notes                                |
+-------------------+--------+--------------------------------------+
| admin/books       | POST   | Add book with MinIO upload           |
| admin/books/{id}  | PUT    | Update book                          |
| admin/books/{id}  | DELETE | Delete book (if not borrowed)        |
| admin/loans       | GET    | View all loans                       |
+-------------------+--------+--------------------------------------+

🔹 Security & Error Handling
  -JWT authentication and RBAC

    Standard HTTP responses:
+-------------------------+
| 400 – Bad Request       |
| 401 – Unauthorized      |
| 403 – Forbidden         |
| 404 – Not Found         |
| 409 – Conflict          |
| 422 – Validation error  |
+-------------------------+

🔹 Project Structure

Project_LMS
├── backend
│   ├── app
│   │   ├── api
│   │   ├── crud
│   │   ├── core
│   │   ├── models
│   │   ├── services
│   │   ├── schema
│   │   └── main.py
│   ├── alembic
│   ├── requirements.txt
│   └── .env
├── frontend_V01
│   ├── public
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   ├── context
│   │   ├── pages
│   │   ├── routes
│   │   ├── styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md


🔹 Developer Commands
Action	Command
Run backend:uvicorn app.main:app --reload
Run frontend:npm run dev
Build frontend	npm run build
Run Docker:docker compose up --build

## 🔹 System Architecture

+-------------------+      HTTP/API       +-------------------+
|   React Frontend  | <----------------> |   FastAPI Backend |
|  SPA + RBAC/Auth  |                    |  Business Logic   |
+-------------------+                    +-------------------+
        |                                      |
        v                                      v
+-------------------+                    +-------------------+
|   PostgreSQL DB   | <----------------> |      MinIO        |
|  Books & Loans    |                    |  PDF/Cover Files  |
+-------------------+                    +-------------------+

![System Architecture](assets/Diagram.png)

System Architecture
🔹 User Flow Diagram

Standard User (Patron)
 -Login/Register → Browse/Search Books → Borrow/Return → Rate/Review

Administrator (Librarian/Staff)
 -Login/Register → Admin Dashboard → Manage Books → Manage Loans → Manage Assets
🔹 Database / ERD (Simplified)

+---------+       +---------+       +---------+
|  Users  |       |  Books  |       |  Loans  |
+---------+       +---------+       +---------+
| id      |<----->| id      |<----->| id      |
| name    |       | title   |       | user_id |
| email   |       | author  |       | book_id |
| role    |       | ISBN    |       | status  |
| password|       | stock   |       | borrowed_at |
+---------+       +---------+       | returned_at |
                                     +---------+

+---------+
| Reviews |
+---------+
| id      |
| user_id |
| book_id |
| rating  |
| text    |
+---------+
# Environment Variables

## 🟦 Backend `.env`

```env
DATABASE_URL=postgresql+asyncpg://postgres:123456@localhost:5432/lmsv01
SECRET_KEY=9YtQ4rK2vH0ePq3xF7gWjZlA6bN1uV8o
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_BORROW_LIMIT=5
ADMIN_EMAIL=admin@library.com
ADMIN_PASSWORD=admin123

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=media

🟦 Frontend .env
VITE_API_BASE_URL=http://localhost:8000
🟦 Root .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_DB=lmsv01
DATABASE_URL=postgresql+asyncpg://postgres:123456@db:5432/lmsv01

MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=media

PGADMIN_DEFAULT_EMAIL=jamilahmediiuc@gmail.com
PGADMIN_DEFAULT_PASSWORD=123456

## 🔹 Docker Compose Setup

Here is the `docker-compose.yml` for running the LMS project with Docker:

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-123456}
      POSTGRES_DB: ${POSTGRES_DB:-lmsv01}
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  minio:
    image: minio/minio:latest
    container_name: minio
    restart: unless-stopped
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY:-minioadmin}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    command: server /data --console-address ":9001"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    depends_on:
      - db
      - minio
    env_file:
      - ./backend/.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-123456}@db:5432/${POSTGRES_DB:-lmsv01}
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY:-minioadmin}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY:-minioadmin}
      MINIO_BUCKET: media
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    command: >
      sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

  frontend:
    build:
      context: ./frontend_V01
      dockerfile: Dockerfile
      args:
        VITE_API_BASE_URL: ${VITE_API_BASE_URL:-http://localhost:8000}
    depends_on:
      - backend
    ports:
      - "5174:80"
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "8080:80"
    depends_on:
      - db

volumes:
  db_data:
  minio_data:

