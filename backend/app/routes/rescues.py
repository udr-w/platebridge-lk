from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import allow,current_user
from ..models import AuditEvent, FoodListing, Incident, Message, Rescue, User
from ..schemas import IncidentCreate, MessageCreate

router=APIRouter(tags=["rescues"])
def rescue_json(r,user):
    recipient_name=r.recipient.alias or "Community member" if r.recipient.anonymous and user.role not in {"admin","coordinator"} else r.recipient.name
    return {c.name:getattr(r,c.name) for c in r.__table__.columns}|{"listing_title":r.listing.title,"recipient_name":recipient_name,"donor_name":r.listing.donor.organisation or r.listing.donor.name}

@router.get("/rescues")
def rescues(db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=select(Rescue).order_by(Rescue.created_at.desc())
    if user.role=="recipient":q=q.where(Rescue.recipient_id==user.id)
    elif user.role=="donor":q=q.join(FoodListing).where(FoodListing.donor_id==user.id)
    elif user.role=="volunteer":q=q.where(or_(Rescue.volunteer_id==user.id,Rescue.status=="VOLUNTEER_NEEDED"))
    elif user.role=="coordinator":q=q.join(FoodListing).where(FoodListing.district==user.district)
    return [rescue_json(r,user) for r in db.scalars(q).all()]

@router.get("/rescues/{rescue_id}")
def rescue_detail(rescue_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    r=db.get(Rescue,rescue_id)
    if not r:raise HTTPException(404,"Rescue not found")
    out=rescue_json(r,user)
    out["messages"]=[{c.name:getattr(m,c.name) for c in m.__table__.columns} for m in db.scalars(select(Message).where(Message.rescue_id==r.id)).all()]
    out["timeline"]=[{c.name:getattr(a,c.name) for c in a.__table__.columns} for a in db.scalars(select(AuditEvent).where(AuditEvent.entity_type=="rescue",AuditEvent.entity_id==r.id)).all()]
    return out

def transition(db,r,user,target,allowed):
    if r.status not in allowed:raise HTTPException(409,f"Cannot move from {r.status} to {target}")
    r.status=target;db.add(AuditEvent(entity_type="rescue",entity_id=r.id,action=target,actor_id=user.id,detail="Demo workflow transition"));db.commit();return {"id":r.id,"status":r.status}

@router.post("/rescues/{rid}/confirm-pickup")
def pickup(rid:int,code:str,db:Session=Depends(get_db),user:User=Depends(allow("donor","volunteer"))):
    r=db.get(Rescue,rid)
    if not r or r.pickup_code!=code:raise HTTPException(400,"Pickup code does not match")
    return transition(db,r,user,"COLLECTED",{"READY_FOR_PICKUP","VOLUNTEER_ASSIGNED"})
@router.post("/rescues/{rid}/confirm-delivery")
def delivered(rid:int,db:Session=Depends(get_db),user:User=Depends(allow("volunteer"))):return transition(db,db.get(Rescue,rid),user,"DELIVERED",{"COLLECTED"})
@router.post("/rescues/{rid}/confirm-receipt")
def received(rid:int,db:Session=Depends(get_db),user:User=Depends(allow("recipient"))):
    r=db.get(Rescue,rid)
    if not r or r.recipient_id!=user.id:raise HTTPException(404,"Rescue not found")
    result=transition(db,r,user,"RECEIVED",{"COLLECTED","DELIVERED"});r.listing.status="COMPLETED" if r.listing.available_portions==0 else r.listing.status;db.commit();return result
@router.post("/rescues/{rid}/cancel")
def cancel(rid:int,db:Session=Depends(get_db),user:User=Depends(allow("recipient"))):
    r=db.get(Rescue,rid)
    if not r or r.recipient_id!=user.id:raise HTTPException(404,"Rescue not found")
    r.listing.available_portions+=r.portions;r.listing.status="AVAILABLE";return transition(db,r,user,"CANCELLED",{"CONFIRMED","VOLUNTEER_NEEDED","READY_FOR_PICKUP"})
@router.get("/volunteer-tasks")
def tasks(db:Session=Depends(get_db),user:User=Depends(allow("volunteer","coordinator","admin"))):return [rescue_json(r,user) for r in db.scalars(select(Rescue).where(Rescue.fulfilment=="delivery",Rescue.status.in_(["VOLUNTEER_NEEDED","VOLUNTEER_ASSIGNED","COLLECTED"]))).all()]
@router.post("/volunteer-tasks/{rid}/accept")
def accept(rid:int,db:Session=Depends(get_db),user:User=Depends(allow("volunteer"))):
    r=db.get(Rescue,rid)
    if not r:raise HTTPException(404,"Task not found")
    r.volunteer_id=user.id;return transition(db,r,user,"VOLUNTEER_ASSIGNED",{"VOLUNTEER_NEEDED"})
@router.post("/incidents")
def incident(body:IncidentCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    if not db.get(Rescue,body.rescue_id):raise HTTPException(404,"Rescue not found")
    i=Incident(**body.model_dump(),reporter_id=user.id);db.add(i);db.flush();r=db.get(Rescue,body.rescue_id);r.flagged=True;db.add(AuditEvent(entity_type="rescue",entity_id=r.id,action="INCIDENT_OPENED",actor_id=user.id,detail=body.category));db.commit();return {"id":i.id,"status":i.status}
@router.post("/rescues/{rid}/messages")
def message(rid:int,body:MessageCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    m=Message(rescue_id=rid,sender_id=user.id,body=body.body);db.add(m);db.commit();return {"id":m.id}

