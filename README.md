# 📚 Library Management System (LMS)

Full-Stack Web Application – A modern digital library platform for managing physical and digital books.  
Supports patrons (users) and administrators (library staff) with full role-based access control (RBAC).

---

## 🔹 Table of Contents
- [Project Overview](#-project-overview)
- [User Roles & Access](#-user-roles--access)
- [Getting Started](#-getting-started)
- [Frontend Overview](#-frontend-overview)
- [Backend Overview](#-backend-overview)
- [Core Features](#-core-features)
- [Technical Stack](#-technical-stack)
- [Routing & State Management](#-routing--state-management)
- [API Endpoints](#-api-endpoints)
- [Security & Error Handling](#-security--error-handling)
- [Project Structure](#-project-structure)
- [Developer Commands](#-developer-commands)
- [Contributing](#-contributing)
- [System Architecture](#-system-architecture)
- [User Flow Diagram](#-user-flow-diagram)
- [Database / ERD (Simplified)](#-database--erd-simplified)
- [License & Contact](#-license--contact)

---

## 🔹 Project Overview
The Library Management System (LMS) is a web-based platform that simplifies management of both physical and digital library resources.

**Goals**
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

## 🔹 Getting Started

### ✅ Prerequisites
- Node.js v18+
- npm or yarn
- Python v3.8+
- PostgreSQL (or SQLite for dev)

### ⚙️ Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload

💻 Frontend Setup

cd frontend
npm install
npm run dev

Access:
Frontend → http://localhost:5173

Backend → http://localhost:8000/docs
🔹 Frontend Overview

    React + Vite + Tailwind CSS + DaisyUI

    Role-based route protection (RoleBasedRoute)

    Global auth via Context API

    Responsive UI

    Axios for API communication

🔹 Backend Overview

    FastAPI + Async SQLAlchemy ORM

    PostgreSQL for DB

    MinIO (S3-compatible) for files

    JWT-based auth + RBAC

    Modular service-repository structure

🔹 Core Features
🧑‍💻 User

    Browse/search books

    Borrow/return books

    Review and rate books

    View loan history

🛠️ Admin

    Manage books and categories

    Manage loans and users

    Upload digital assets (PDFs, covers)

🔹 Technical Stack
Layer	Technology
Frontend	React + Vite + Tailwind CSS + DaisyUI
Routing	React Router DOM v6
State	React Context API
HTTP	Axios
Backend	FastAPI
ORM	SQLAlchemy (Async)
Database	PostgreSQL
File Storage	MinIO
Auth	JWT, RBAC
🔹 Routing & State Management

    Role-based protected routes

    AuthProvider manages login state

    Layouts for each role (Admin/User)

🔹 API Endpoints
📦 Authentication & User Interaction
Endpoint	Method	Body / Query	Response	Notes
auth/register	POST	email, password	201 Created	409 if exists
auth/login	POST	email, password	200 OK (JWT)	401 Unauthorized
books/rate/{id}	POST	rating, review_text	201 Created	400 if already rated
📦 Catalog & Borrowing
Endpoint	Method	Notes
books	GET	Query: category, search, pagination
books/{id}	GET	Book details
books/borrow/{id}	POST	Borrow a book (auth)
books/return/{id}	POST	Return a book (auth)
📦 Admin Operations
Endpoint	Method	Notes
admin/books	POST	Add book (MinIO upload)
admin/books/{id}	PUT	Update book
admin/books/{id}	DELETE	Delete if not borrowed
admin/loans	GET	View all loans
🔹 Security & Error Handling

    JWT auth and RBAC

    Standard responses:
    400, 401, 403, 404, 409, 422

🔹 Project Structure

Project_LMS
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── models
│   │   ├── services
│   │   └── main.py
│   ├── alembic
│   ├── requirements.txt
│   └── .env
├── frontend
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
└── README.md

🔹 Developer Commands
Action	Command
Run backend	uvicorn app.main:app --reload
Run frontend	npm run dev
Build frontend	npm run build
Lint frontend	npx eslint . --ext .js,.jsx
Format code	npx prettier --write .
🔹 Contributing

    Fork the repo

    Create a branch feature/your-feature

    Commit & push changes

    Open a Pull Request

🔹 System Architecture

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

🔹 User Flow Diagram

User (Patron):
Login → Browse → Borrow → Return → Review

Admin (Librarian):
Login → Dashboard → Manage Books → Manage Loans
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
