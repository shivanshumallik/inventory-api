# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings


def register_user(db: Session, user_data: UserRegister) -> UserResponse:
    """Register a new user"""
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_data.email}' is already registered"
        )

    hashed = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed,
        role=user_data.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
    """Authenticate user and return JWT token"""
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


def get_all_users(db: Session) -> list[User]:
    """Get all users — admin only"""
    return db.query(User).all()