from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import allow,current_user
from ..models import CollectionPoint, FoodListing, Incident, Notification, Rescue, SafetyRule, User
from ..schemas import UserOut
from ..seed import reset_database

router=APIRouter(tags=["platform"])
@router.get("/users/me",response_model=UserOut)
def me(user:User=Depends(current_user)):return user
@router.patch("/profiles/privacy")
def privacy(anonymous:bool,alias:str|None=None,db:Session=Depends(get_db),user:User=Depends(allow("recipient"))):
    user.anonymous=anonymous
    if alias:user.alias=alias
    db.commit();return {"anonymous":user.anonymous,"alias":user.alias}
@router.get("/collection-points")
def points(db:Session=Depends(get_db),user:User=Depends(current_user)):return [{c.name:getattr(x,c.name) for c in x.__table__.columns} for x in db.scalars(select(CollectionPoint).where(CollectionPoint.active==True)).all()]
@router.get("/notifications")
def notifications(db:Session=Depends(get_db),user:User=Depends(current_user)):return [{c.name:getattr(x,c.name) for c in x.__table__.columns} for x in db.scalars(select(Notification).where(Notification.user_id==user.id).order_by(Notification.created_at.desc())).all()]
@router.get("/incidents")
def incidents(db:Session=Depends(get_db),user:User=Depends(allow("coordinator","admin"))):return [{c.name:getattr(x,c.name) for c in x.__table__.columns} for x in db.scalars(select(Incident).order_by(Incident.created_at.desc())).all()]
@router.patch("/incidents/{iid}")
def update_incident(iid:int,status:str,notes:str="",db:Session=Depends(get_db),user:User=Depends(allow("coordinator","admin"))):
    i=db.get(Incident,iid)
    if not i:raise HTTPException(404,"Incident not found")
    i.status=status;i.coordinator_notes=notes;db.commit();return {"id":i.id,"status":i.status}
@router.get("/metrics/dashboard")
def metrics(db:Session=Depends(get_db),user:User=Depends(current_user)):
    completed=db.scalar(select(func.coalesce(func.sum(Rescue.portions),0)).where(Rescue.status=="RECEIVED"))
    return {"portions_rescued":completed,"active_listings":db.scalar(select(func.count()).select_from(FoodListing).where(FoodListing.status=="AVAILABLE")),"available_portions":db.scalar(select(func.coalesce(func.sum(FoodListing.available_portions),0)).where(FoodListing.status=="AVAILABLE")),"completed_rescues":db.scalar(select(func.count()).select_from(Rescue).where(Rescue.status=="RECEIVED")),"active_donors":db.scalar(select(func.count()).select_from(User).where(User.role=="donor",User.active==True)),"active_volunteers":db.scalar(select(func.count()).select_from(User).where(User.role=="volunteer",User.active==True)),"open_incidents":db.scalar(select(func.count()).select_from(Incident).where(Incident.status!="RESOLVED")),"estimated_note":"Activity counts are from demo records; no scientific environmental claim is made."}
@router.get("/admin/users")
def users(db:Session=Depends(get_db),user:User=Depends(allow("admin"))):return [{c.name:getattr(x,c.name) for c in x.__table__.columns} for x in db.scalars(select(User).order_by(User.role,User.name)).all()]
@router.patch("/admin/users/{uid}/active")
def activate(uid:int,active:bool,db:Session=Depends(get_db),user:User=Depends(allow("admin"))):
    target=db.get(User,uid)
    if not target:raise HTTPException(404,"User not found")
    target.active=active;db.commit();return {"id":uid,"active":active}
@router.get("/admin/safety-rules")
def rules(db:Session=Depends(get_db),user:User=Depends(allow("admin"))):return [{c.name:getattr(x,c.name) for c in x.__table__.columns} for x in db.scalars(select(SafetyRule)).all()]
@router.patch("/admin/safety-rules/{rid}")
def rule(rid:int,value:str,db:Session=Depends(get_db),user:User=Depends(allow("admin"))):
    x=db.get(SafetyRule,rid)
    if not x:raise HTTPException(404,"Rule not found")
    x.value=value;db.commit();return {"id":rid,"value":value,"note":"Restart backend for environment-backed rule changes."}
@router.post("/demo/reset")
def reset(db:Session=Depends(get_db),user:User=Depends(allow("admin"))):
    db.close()
    reset_database()
    return {"status":"reset","message":"Demo dataset restored. Please sign in again."}
