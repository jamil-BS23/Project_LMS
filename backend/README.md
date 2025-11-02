 📚 Library Management System – Backend

 🔹 Project Overview

The **Library Management System (LMS)** backend is a high-performance REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **MinIO**.  

It provides secure **user authentication**, **role-based access control (RBAC)**, and full CRUD operations for managing library resources.  

🎯 Goals:
- **Users:** Search books, borrow/return, submit reviews and ratings.
- **Admins:** Add/edit/delete books, manage loans, monitor user activity.
- **Library:** Centralized record management and data integrity.

---

## ⚙️ Technology Stack

| Component          | Technology         | Description                                   |
|-------------------|------------------|-----------------------------------------------|
| **Backend**       | FastAPI           | High-performance async API framework         |
| **Database**      | PostgreSQL        | Relational database for persistent storage   |
| **ORM**           | SQLAlchemy (Async)| Async ORM for database models                |
| **Object Storage**| MinIO             | S3-compatible storage for book assets       |
| **Authentication**| JWT               | Secure authentication and RBAC               |
| **Language**      | Python 3.10+      | Backend implementation language              |

---

📂 Project Structure

```text
backend
├── app
│   ├── api               
│   ├── core            
│   ├── models           
│   ├── schemas          
│   ├── services          
│   ├── repository        
│   ├── utils           
│   └── main.py          
├── requirements.txt
└── .env.example

1. Create and Activate Virtual Environment
-bash
-Copy code
-python -m venv venv
-source venv/bin/activate  
-venv\Scripts\activate
     
2. Install Dependencies:
bash
Copy code
pip install -r requirements.txt
3. Configure Environment Variables
 -Create a .env file in the backend/ directory with the following:

-Variable	Description
-DATABASE_URL	PostgreSQL connection string
-SECRET_KEY	JWT secret key
-ALGORITHM	JWT algorithm (e.g., HS256)
-ACCESS_TOKEN_EXPIRE_MINUTES	Token expiration time
-MINIO_ENDPOINT	MinIO server URL

Example:

-env
-Copy code
-DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/library_db=??
-SECRET_KEY=your_secret_key
-ALGORITHM=HS256
-ACCESS_TOKEN_EXPIRE_MINUTES=60
-MINIO_ENDPOINT=http://localhost:9000
-MINIO_ACCESS_KEY=minioadmin
-MINIO_SECRET_KEY=minioadmin
-MINIO_BUCKET_NAME=book-assets

4. Run the Server:
-bash
-Copy code
-uvicorn app.main:app --reload
-Server runs at: http://127.0.0.1:8000
-Swagger UI: http://127.0.0.1:8000/docs

🧩 Core Features
👥 Authentication & Roles
-Register and login using JWT
-Two roles: User (Patron) and Admin (Librarian)
-Role-Based Access Control (RBAC) using FastAPI dependencies

📚 User Operations
-Browse and search books by title, author, ISBN, or category
-Borrow and return books
-Submit ratings and reviews

🧑‍💼 Admin Operations
-Add, edit, and delete books
-Manage loans and track user activity
-Upload digital assets (book covers, PDFs) to MinIO

📦 API Endpoints:
Authentication
Endpoint	Method	Description
-auth/register	POST	Register a new user
-auth/login	POST	Login and receive JWT token

Books:
Endpoint	Method	Description
-books	GET	Browse catalog
-books/{id}	GET	Get book details
-books/borrow/{id}	POST	Borrow a book
-books/return/{id}	POST	Return borrowed book
-books/rate/{id}	POST	Submit rating/review

Admin:
Endpoint	Method	Description
-admin/books	POST	Add a new book (with MinIO upload)
-admin/books/{id}	PUT	Update book details
-admin/books/{id}	DELETE	Remove a book
-admin/loans	GET	View all loan records

🛠️ Error Handling & Security:
Status	Meaning	Example
-400	Bad Request	Invalid input or duplicate action
-401	Unauthorized	Missing/invalid JWT
-403	Forbidden	Role access denied
-404	Not Found	Resource not found
-409	Conflict	Duplicate email or business rule
-422	Validation Error	Invalid request payload

Security:
-JWT token authentication
-Role-based authorization
-Input validation via Pydantic
-Secure file uploads with MinIO

💻 Developer Commands:
Action	Command
-Run server-	uvicorn app.main:app --reload
-Format code	black .

