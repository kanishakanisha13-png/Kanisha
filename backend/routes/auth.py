import hashlib
import secrets

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.database import get_connection
from backend.services.recommendation_service import get_recommendation_history


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================
# Password Hashing
# =========================

def hash_password(password: str, salt: str | None = None) -> str:

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:

    try:

        salt, original_hash = stored_hash.split("$", 1)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()

        return secrets.compare_digest(
            password_hash,
            original_hash
        )

    except ValueError:

        return False


# =========================
# Register Page
# =========================

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )


# =========================
# Register User
# =========================

@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password_hash
            )
        )

        connection.commit()

    except Exception as e:

        connection.close()

        print("Registration error:", e)

        return RedirectResponse(
            url="/register",
            status_code=303
        )

    connection.close()

    print("New user registered:")
    print("Username:", username)
    print("Email:", email)

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# =========================
# Login Page
# =========================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


# =========================
# Login User
# =========================

@router.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    if not verify_password(
        password,
        user["password_hash"]
    ):

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Store user information in session
    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["email"] = user["email"]
    request.session["logged_in"] = True

    print("Login successful:")
    print("Username:", user["username"])
    print("Email:", user["email"])

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# =========================
# Dashboard Page
# =========================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "username": request.session.get("username"),
            "email": request.session.get("email")
        }
    )


# =========================
# History Page
# =========================

@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):

    user_id = request.session.get("user_id")

    history = get_recommendation_history(
        user_id=user_id
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "history": history
        }
    )


# =========================
# Session Information
# =========================

@router.get("/session-info")
async def session_info(request: Request):

    return {
        "logged_in": request.session.get(
            "logged_in",
            False
        ),
        "username": request.session.get(
            "username"
        ),
        "email": request.session.get(
            "email"
        )
    }


# =========================
# Session Data
# =========================

@router.get("/session-data")
async def session_data(request: Request):

    return {
        "session": dict(request.session)
    }


# =========================
# Logout User
# =========================

@router.get("/logout")
async def logout_user(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )