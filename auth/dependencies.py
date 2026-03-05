from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from six import reraise
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from auth.jwt import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is  None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")

    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    """Verify that the current user is an admin.
       Use this as a dependency on admin-only endpoints."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required. You do not have permission to perform this action."
        )
    return current_user