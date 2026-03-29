# app/routers/auth.py

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services import auth_service
from app.models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    return auth_service.register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with JSON body.
    Use this from your frontend or Postman.
    """
    return auth_service.login_user(db, login_data)


@router.post("/token", response_model=TokenResponse)
def login_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint for Swagger UI OAuth2 form.
    Swagger sends username/password as form data — this handles that.
    'username' field = your email address.
    """
    from app.schemas.user import UserLogin
    login_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    return auth_service.login_user(db, login_data)


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the currently logged in user's profile."""
    return current_user


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users — ADMIN ONLY."""
    return auth_service.get_all_users(db)