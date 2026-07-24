import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import allow, current_user
from ..models import AuditEvent, FoodListing, Rescue, User
from ..schemas import ClaimCreate, ListingCreate
from ..safety import assess_food

router=APIRouter(prefix="/listings",tags=["listings"])
def listing_json(l, user=None):
    distance=None
    if user:
        p1,p2=math.radians(user.latitude),math.radians(l.latitude); dp=math.radians(l.latitude-user.latitude); dl=math.radians(l.longitude-user.longitude)
        distance=round(6371*2*math.atan2(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2),math.sqrt(1-(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))),1)
    return {c.name:getattr(l,c.name) for c in l.__table__.columns}|{"donor_name":l.donor.organisation or l.donor.name,"distance_km":distance}

@router.get("")
def all_listings(status: str|None=None, district: str|None=None, db:Session=Depends(get_db), user:User=Depends(current_user)):
    q=select(FoodListing).order_by(FoodListing.created_at.desc())
    if user.role=="recipient": q=q.where(FoodListing.status=="AVAILABLE",FoodListing.collection_deadline>datetime.utcnow())
    elif user.role=="donor": q=q.where(FoodListing.donor_id==user.id)
    if status: q=q.where(FoodListing.status==status)
    if district: q=q.where(FoodListing.district==district)
    return [listing_json(x,user) for x in db.scalars(q).all()]

@router.post("")
def create_listing(body:ListingCreate,db:Session=Depends(get_db),user:User=Depends(allow("donor"))):
    result=assess_food(body)
    status={"GREEN":"AVAILABLE","AMBER":"PENDING_COORDINATOR_REVIEW","RED":"REJECTED"}[result["classification"]]
    l=FoodListing(**body.model_dump(),donor_id=user.id,available_portions=body.portions,classification=result["classification"],safety_explanation=result["explanation"],failed_checks=" | ".join(result["failed_checks"]),status=status)
    db.add(l);db.flush();db.add(AuditEvent(entity_type="listing",entity_id=l.id,action="SAFETY_CHECK_COMPLETED",actor_id=user.id,detail=result["explanation"]));db.commit();db.refresh(l)
    return listing_json(l,user)

@router.get("/{listing_id}")
def get_listing(listing_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    l=db.get(FoodListing,listing_id)
    if not l: raise HTTPException(404,"Listing not found")
    data=listing_json(l,user)
    data["timeline"]=[{c.name:getattr(a,c.name) for c in a.__table__.columns} for a in db.scalars(select(AuditEvent).where(AuditEvent.entity_type=="listing",AuditEvent.entity_id==listing_id).order_by(AuditEvent.created_at)).all()]
    return data

@router.patch("/{listing_id}")
def edit_listing(listing_id:int,body:ListingCreate,db:Session=Depends(get_db),user:User=Depends(allow("donor"))):
    l=db.get(FoodListing,listing_id)
    if not l or l.donor_id!=user.id: raise HTTPException(404,"Listing not found")
    if l.status not in {"DRAFT","PENDING_COORDINATOR_REVIEW","AVAILABLE"}: raise HTTPException(409,"This listing can no longer be edited")
    for k,v in body.model_dump().items(): setattr(l,k,v)
    result=assess_food(body); l.classification=result["classification"];l.safety_explanation=result["explanation"];l.failed_checks=" | ".join(result["failed_checks"]);l.status={"GREEN":"AVAILABLE","AMBER":"PENDING_COORDINATOR_REVIEW","RED":"REJECTED"}[l.classification]
    db.commit();return listing_json(l,user)

@router.post("/{listing_id}/cancel")
def cancel(listing_id:int,db:Session=Depends(get_db),user:User=Depends(allow("donor"))):
    l=db.get(FoodListing,listing_id)
    if not l or l.donor_id!=user.id: raise HTTPException(404,"Listing not found")
    if l.status not in {"AVAILABLE","PENDING_COORDINATOR_REVIEW"}: raise HTTPException(409,"Listing cannot be cancelled")
    l.status="CANCELLED";db.commit();return {"status":l.status}

@router.post("/{listing_id}/approve")
def approve(listing_id:int,db:Session=Depends(get_db),user:User=Depends(allow("coordinator","admin"))):
    l=db.get(FoodListing,listing_id)
    if not l or l.status!="PENDING_COORDINATOR_REVIEW": raise HTTPException(409,"Listing is not awaiting review")
    l.status="AVAILABLE";db.add(AuditEvent(entity_type="listing",entity_id=l.id,action="LISTING_APPROVED",actor_id=user.id,detail="Approved after coordinator demo review"));db.commit();return listing_json(l,user)

@router.post("/{listing_id}/reject")
def reject(listing_id:int,db:Session=Depends(get_db),user:User=Depends(allow("coordinator","admin"))):
    l=db.get(FoodListing,listing_id)
    if not l: raise HTTPException(404,"Listing not found")
    l.status="REJECTED";db.commit();return listing_json(l,user)

@router.post("/{listing_id}/claim")
def claim(listing_id:int,body:ClaimCreate,db:Session=Depends(get_db),user:User=Depends(allow("recipient"))):
    l=db.get(FoodListing,listing_id)
    if not l or l.status!="AVAILABLE" or l.collection_deadline<=datetime.utcnow(): raise HTTPException(409,"This listing is no longer available")
    if body.portions>l.available_portions: raise HTTPException(409,"Requested portions are not available")
    l.available_portions-=body.portions
    if l.available_portions==0:l.status="RESERVED"
    r=Rescue(listing_id=l.id,recipient_id=user.id,portions=body.portions,fulfilment=body.fulfilment,collection_point_id=body.collection_point_id,pickup_code=f"PB{(l.id*941+user.id*37)%10000:04d}",status="VOLUNTEER_NEEDED" if body.fulfilment=="delivery" else "READY_FOR_PICKUP")
    db.add(r);db.flush();db.add(AuditEvent(entity_type="listing",entity_id=l.id,action="LISTING_CLAIMED",actor_id=user.id,detail=f"{body.portions} portions; {body.fulfilment}"));db.commit()
    return {"id":r.id,"pickup_code":r.pickup_code,"status":r.status}

