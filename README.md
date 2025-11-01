📚 Library Management System (LMS)
Full-Stack Web Application – A modern digital library platform for managing physical and digital books.
Supports patrons (users) and administrators (library staff) with full role-based access control (RBAC).
🔹 Table of Contents
Project Overview
User Roles & Access
Getting Started
🔹 Project Overview
The Library Management System (LMS) is a web-based platform that simplifies management of both physical and digital library resources.

🎯 Goals
Users: Search, borrow, return books, submit reviews.
Admins: Manage inventory, users, and assets.

🔹 User Roles & Access
👤 Standard User (Patron)
 -Search and browse books
 -Borrow and return books
 -View borrowing history
 -Submit ratings and reviews
 
🧭 Administrator (Librarian / Staff)
 -All standard user permissions
 -Add, update, delete books
 -Manage categories 
 -View all loans and user activity
🔹 Getting Started
✅ Prerequisites
Node.js v18+
npm or yarn
Python v3.8+
PostgreSQL

⚙️ Backend Setup
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
👥 User Features:
   -Search/browse books by title, author, or ISBN
   -Borrow and return books
   -Rate and review titles
   -personal loan history

🛠️ Admin Features:
   -Add, edit, delete books and categories
   -Manage user loans and assets
   -Upload and organize digital media (PDFs, covers)
   

🔹 Technical Stack:
  -Frontend	React + Vite + Tailwind CSS + DaisyUI
  -Routing	React Router DOM v6
  -State Management	React Context API
  -HTTP Client	Axios
  -Backend	FastAPI
  -ORM	SQLAlchemy (Async)
  -Database	PostgreSQL
  -File Storage	MinIO
  -Authentication	JWT, RBAC
  
🔹 Routing & State Management:
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
|   |   ├── crud
│   │   ├── core  
│   │   ├── models    
│   │   ├── services
|   |   ├── schema
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
Run backend:uvicorn app.main:app --reload
Run frontend:npm run dev
Build frontend	npm run build

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
