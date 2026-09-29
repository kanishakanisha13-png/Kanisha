import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from backend.database import create_tables

from backend.routes.home import router as home_router
from backend.routes.party import router as party_router
from backend.routes.jewelry import router as jewelry_router
from backend.routes.auth import router as auth_router


# =========================
# Load Environment Variables
# =========================

load_dotenv()

SESSION_SECRET_KEY = os.getenv(
    "SESSION_SECRET_KEY",
    "pocketsmart-secret-key-2026"
)


# =========================
# Create Database Tables
# =========================

create_tables()


# =========================
# FastAPI Application
# =========================

app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Recommendation Assistant",
    version="1.0.0"
)


# =========================
# Session Management
# =========================

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=3600
)


# =========================
# Static Files
# =========================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================
# Jinja2 Templates
# =========================

templates = Jinja2Templates(
    directory="templates"
)


# =========================
# Include Routers
# =========================

app.include_router(home_router)
app.include_router(party_router)
app.include_router(jewelry_router)
app.include_router(auth_router)


# =========================
# Home Page
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================
# Health Check
# =========================

@app.get("/health")
async def health_check():

    return {
        "status": "success",
        "message": "PocketSmart AI backend is running"
    }


# =========================
# Run Application
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )