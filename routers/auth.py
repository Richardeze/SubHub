from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.wallet import Wallet
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from schemas.auth import RegisterRequest, AuthResponse, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse)
def register(data: RegisterRequest, db: Session=Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered, Please login instead.")



    # Hash password
    hashed_pw = hash_password(data.password)

    # Create user
    new_user = User(email=data.email,
                    hashed_password=hashed_pw,
                    is_admin=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create wallet automatically
    wallet = Wallet(user_id=new_user.id)
    db.add(wallet)
    db.commit()

    # Create JWT token
    access_token = create_access_token(data={"user_id": new_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=AuthResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify Password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create token
    access_token = create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }