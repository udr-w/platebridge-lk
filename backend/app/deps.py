from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

def current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer demo-"):
        raise HTTPException(401, "Use a demo account to sign in")
    try:
        user_id = int(authorization.removeprefix("Bearer demo-"))
    except ValueError:
        raise HTTPException(401, "Invalid demo token")
    user = db.get(User, user_id)
    if not user or not user.active:
        raise HTTPException(403, "Demo account is unavailable")
    return user

def allow(*roles):
    def check(user: User = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(403, "This action is not available for your demo role")
        return user
    return check

