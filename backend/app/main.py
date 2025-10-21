from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import borrow, books   # ✅ fixed here
from app.database import Base, engine
import asyncio

app = FastAPI(
    title="Library Management System",
    description="Async LMS Backend API with Borrow & Book Features",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(books.router)  
app.include_router(borrow.router)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()

@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System API"}
