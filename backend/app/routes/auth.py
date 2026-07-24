from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..config import DEMO_PASSWORD
from ..database import get_db
from ..models import User
from ..schemas import DemoLogin

router=APIRouter(prefix="/auth",tags=["authentication"])
@router.post("/demo-login")
def demo_login(body: DemoLogin, db: Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==body.email))
    if body.password != DEMO_PASSWORD or not user:
        raise HTTPException(401,"Incorrect demo account or password")
    if not user.active: raise HTTPException(403,"This demo account is suspended")
    return {"access_token":f"demo-{user.id}","token_type":"bearer","user":{"id":user.id,"email":user.email,"name":user.name,"role":user.role,"language":user.language}}

