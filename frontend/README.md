# 📚 Library Management System – Frontend

## 🔹 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [User Roles](#user-roles)
4. [Getting Started](#getting-started)
5. [Project Structure](#project-structure)
6. [Technical Stack](#technical-stack)
7. [Routing & State Management](#routing--state-management)
8. [API Integration](#api-integration)
9. [Developer Commands](#developer-commands)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact](#contact)

---

## 🔹 Project Overview

The frontend of the **Library Management System (LMS)** is a **Single-Page Application (SPA)** built with **React + Vite + Tailwind/DaisyUI**. It provides a responsive interface for both **library patrons** and **administrators**.

**Goals:**
- Enable users to search, browse, borrow/return books, and submit reviews.
- Provide admins the ability to manage books, categories, loans, and track user activity.
- Implement role-based access control (RBAC) for secure operations.

**Screenshots (Placeholder):**
![Home Page](./screenshots/home.png)
![Admin Dashboard](./screenshots/admin_dashboard.png)

---

## 🔹 Features
- Browse and search books by **title, author, ISBN, or category**
- Borrow and return books
- Submit ratings and reviews
- Admin dashboard: Add, edit, delete books and manage loans
- Role-based route protection
- Fully responsive design (desktop & mobile)

---

## 🔹 User Roles

### Standard User (Patron)
- Browse and search books  
- Borrow/return books  
- View borrowing history  
- Submit ratings and reviews  

### Administrator (Librarian/Staff)
- All standard user permissions  
- Add, edit, delete books  
- Manage book categories and digital assets  
- View all active and historical loans  

---

## 🔹 Getting Started

### Prerequisites
- Node.js v18+  
- npm or yarn  
- Backend API running (FastAPI recommended)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/library-management-frontend.git
cd library-management-frontend
Install dependencies:

bash
Copy code
npm install
# or
yarn install
Configure environment variables:

env
Copy code
# Create a .env file in the project root
VITE_API_BASE_URL=http://localhost:8000
Start the development server:

bash
Copy code
npm run dev
# or
yarn dev
App runs at http://localhost:5173

🔹 Project Structure
text
Copy code
frontend/
├── public/           # Static assets (images, fonts)
├── src/
│   ├── api/          # Axios instance & HTTP utilities
│   ├── components/   # Reusable UI components
│   ├── context/      # AuthProvider & global state
│   ├── pages/        # Views / pages (Home, BookDetails, Admin)
│   ├── routes/       # Role-based routing & protected routes
│   ├── styles/       # Tailwind/DaisyUI custom styles
│   └── main.jsx      # App entry point
├── index.html
├── package.json
└── vite.config.js
🔹 Technical Stack
Component	Technology	Purpose
Framework	React (Functional Hooks)	UI rendering
Build Tool	Vite	Fast dev & HMR
Routing	React Router DOM v6	SPA navigation
Styling	Tailwind CSS & DaisyUI	Responsive UI & prebuilt components
State Management	React Context API	Global auth & role state
HTTP Client	Axios	API integration with backend

🔹 Developer Commands
Action	Command
Run frontend:	npm run dev 
Build production:	npm run build 
Format code	npx prettier --write .
Lint code	npx eslint . --ext .js,.jsx
Run tests	npm run test / yarn test

🔹 Contributing
Fork the repository

Create a feature/bugfix branch

Commit your changes

Push and submit a pull request