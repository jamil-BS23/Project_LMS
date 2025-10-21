from fastapi import FastAPI
from app.api.borrow import router as borrow_router
from app.database import Base, engine
import asyncio

app = FastAPI(title="Library API", version="1.0")

# Include your router
app.include_router(borrow_router)

@app.get("/")
def root():
    return {"message": "Library API running!"}

# Async table creation
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Run table creation before app starts
asyncio.run(init_models())
