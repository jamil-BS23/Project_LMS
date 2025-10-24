📚 Library Management System
Project Structure
LMS_Project/
├── backend/
│   ├── app/
│   │   ├── main.py          
│   │   ├── models.py         
│   │   ├── schemas.py        
│   │   ├── crud.py          
│   │   └── database.py       
│   ├── requirements.txt      
├── frontend/
│   ├── public/
│   └── src/
│       ├── App.jsx          
│       ├── index.jsx         
│       └── components/
│           └── BookCard.jsx 
│   ├── package.json         
└── README.md


Backend Code 
backend/requirements.txt
fastapi
uvicorn
sqlalchemy
pydantic

Backend Run
cd backend
uvicorn app.main:app --reload

# 📚 Library Management System (LMS)

**Full-Stack Minimal Example** – Digital library platform for managing books.

## Features
- View books
- Add new books (admin)
- Simple React frontend + FastAPI backend
- PostgreSQL database

## Getting Started

### Backend
```bash
cd backend
python -m venv .venv
# activate
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/macOS

pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend Run
cd frontend
npm install
npm run dev

Access frontend: http://localhost:5173
 Access backend: http://localhost:8000

