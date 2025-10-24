 📚 Library Management System (LMS)

Full-Stack Web Application – Modern digital library platform for managing physical and digital books.  
Supports patrons (users) and administrators (library staff) with full role-based access control (RBAC).

 🔹 Table of Contents
1. [Project Overview]
2. [User Roles & Access]
3. [Getting Started]
4. [Frontend Overview]
5. [Backend Overview]
6. [Core Features]
7. [Technical Stack]
8. [Routing & State Management]
9. [API Endpoints]
10. [Security & Error Handling]
11. [Project Structure]
12. [Developer Commands]
13. [Contributing]
14. [License]
15. [Contact]

🔹 Project Overview

The Library Management System is a modern web-based application designed to manage a library’s physical and digital books efficiently.  

Goals:
 For Users: Search, borrow/return books, manage personal loans, submit reviews.
 For Administrators: Manage books, track loans, view user activity, manage digital assets.
 For the Library: Centralized records ensuring accurate book stock tracking and engagement monitoring.

Screenshots (Placeholder):
[Home Page] 
[Admin Dashboard]

🔹 User Roles & Access
 Standard User (Patron)
- Search and browse the catalog  
- Borrow and return books  
- View borrowing history  
- Submit ratings and reviews  

Administrator (Librarian/Staff)
- Full standard user permissions  
- Add, update, delete books  
- Manage categories and digital assets (PDFs, cover images)  
- View all active and historical loan records
- 
 🔹 Getting Started
 Prerequisites
- Node.js v18+  
- npm or yarn  
- Python v3.8+  
- PostgreSQL (optional, SQLite supported for development)

Backend Setup
```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
 Edit .env with your database and MinIO credentials

alembic upgrade head

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Frontend Setup

cd frontend
npm install

Start frontend server
npm run de

Access:

    Frontend at http://localhost:5173
    Backend at http://localhost:8000/doc

🔹 Frontend Overview

    SPA built with React + Vite + Tailwind CSS & DaisyUI

    Role-based route protection (RoleBasedRoute)

    Global state management via React Context API (AuthProvider)

    Responsive mobile-first design

    Centralized Axios instance for API communication

🔹 Backend Overview

    FastAPI with asynchronous SQLAlchemy ORM

    PostgreSQL for relational data storage

    MinIO (S3-compatible) for binary files (book covers, PDFs)

    Modular architecture with service/repository pattern

    JWT-based authentication & RBAC for security

🔹 Core Features
User Features

    Search/browse books by title, author, ISBN, or category

    Borrow and return books

    Submit ratings and reviews

    View personal borrowing history

Admin Features

    Add, update, delete books

    Manage categories

    Track loans and user activity

    Upload book assets to MinIO

🔹 Technical Stack
Layer	Technology
Frontend	React + Vite + Tailwind CSS/DaisyUI
Routing	React Router DOM v6
State Management	React Context API
HTTP Client	Axios
Backend	FastAPI
ORM	SQLAlchemy (Async)
Database	PostgreSQL
File Storage	MinIO
Authentication	JWT, RBAC
🔹 Routing & State Management

    Role-based Route Protection: Conditional rendering based on user roles

    AuthProvider: Manages global authentication state

    Layout Shells: Conditional display of navbar/sidebar based on route

🔹 API Endpoints (Highlights)
Authentication & User Interaction
Endpoint	Method	Body/Query	Response	Notes
auth/register	POST	email, password	201 Created	Error 409 if email exists
auth/login	POST	email, password	200 OK (JWT)	401 Unauthorized
books/rate/{id}	POST	rating, review_text	201 Created	400 if already rated
Catalog & Borrowing
Endpoint	Method	Notes
books	GET	Query: category, search, pagination
books/{id}	GET	Detailed book info
books/borrow/{id}	POST	Borrow a book (auth only)
books/return/{id}	POST	Return a book (auth only)
Admin Operations
Endpoint	Method	Notes
admin/books	POST	Add book with MinIO upload
admin/books/{id}	PUT	Update book
admin/books/{id}	DELETE	Delete book (if not borrowed)
admin/loans	GET	View all loans
🔹 Security & Error Handling

    JWT Authentication & Role-based Access Control

    Standard HTTP response codes:

        400 Bad Request – Client-side error

        401 Unauthorized – Authentication failure

        403 Forbidden – Unauthorized access

        404 Not Found – Resource missing

        409 Conflict – Business rules violated

        422 Unprocessable Entity – Validation errors

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
Run backend:	uvicorn app.main:app --reload
Run frontend:	npm run dev 
Build frontend	npm run build 
Lint frontend	npx eslint . --ext .js,.jsx
Format code	npx prettier --write .
🔹 Contributing

    Fork the repository

    Create a feature/bugfix branch

    Commit your changes

    Push and submit a Pull Request

🔹 System Architecture

+-------------------+      HTTP/API       +-------------------+
|   React Frontend  | <----------------> |   FastAPI Backend |
|  SPA + RBAC/Auth  |                    |  Business Logic  |
+-------------------+                    +-------------------+
        |                                      |
        |                                      |
        v                                      v
+-------------------+                    +-------------------+
|      PostgreSQL   | <----------------> |      MinIO        |
|    Book & Loan DB |                    |  Book Assets (PDFs, Covers) |
+-------------------+                    +-------------------+

🔹 User Flow Diagram
Standard User (Patron)

Login/Register
      |
      v
Browse/Search Books
      |
      v
Borrow Book <--> Return Book
      |
      v
Rate & Review

Administrator (Librarian/Staff)

Login/Register
      |
      v
Admin Dashboard
  |       |       |
  v       v       v
Manage Books   Manage Loans   Manage Assets

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

