from datetime import datetime, timedelta
from sqlalchemy import delete
from .database import Base, SessionLocal, engine
from .models import AuditEvent, CollectionPoint, FoodListing, Incident, Message, Notification, Rescue, SafetyRule, User

ACCOUNTS = [
 ("donor.home@platebridge.demo","Nimali Perera","donor","household",None,"Galle","Karapitiya","si","Garden Table"),
 ("donor.business@platebridge.demo","Ashan Fernando","donor","organisation","Harbour Hearth Bakery (Fictional)","Galle","Galle Fort","en",None),
 ("recipient@platebridge.demo","Maya Silva","recipient",None,None,"Galle","Dadalla","en","Maya G."),
 ("volunteer@platebridge.demo","Kavin Raj","volunteer",None,None,"Galle","Unawatuna","ta",None),
 ("coordinator@platebridge.demo","Tharushi Jayasinghe","coordinator",None,"Southern Community Link (Fictional)","Galle","Galle Fort","en",None),
 ("admin@platebridge.demo","Demo Administrator","admin",None,None,"Colombo","Colombo 05","en",None),
 ("home2@platebridge.demo","Fathima Niyas","donor","household",None,"Matara","Weligama","en",None),
 ("canteen@platebridge.demo","Ruwan Dissanayake","donor","organisation","Lotus Office Canteen (Fictional)","Colombo","Colombo 05","en",None),
 ("recipient2@platebridge.demo","S. Kumari","recipient",None,None,"Galle","Hikkaduwa","si","Sunbird"),
 ("recipient3@platebridge.demo","Arul Selvan","recipient",None,None,"Jaffna","Nallur","ta","A. Selvan"),
 ("volunteer2@platebridge.demo","Ishara Madushani","volunteer",None,None,"Galle","Hapugala","si",None),
 ("volunteer3@platebridge.demo","Rizwan Ahamed","volunteer",None,None,"Colombo","Dehiwala","ta",None),
 ("coordinator2@platebridge.demo","Vinoja Tharmalingam","coordinator",None,"North Community Circle (Fictional)","Jaffna","Nallur","ta",None),
]

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    now = datetime.utcnow()
    users=[]
    for email,name,role,donor_type,org,district,area,lang,alias in ACCOUNTS:
        u=User(email=email,name=name,role=role,donor_type=donor_type,organisation=org,district=district,area=area,language=lang,alias=alias,anonymous=email=="recipient@platebridge.demo")
        db.add(u); users.append(u)
    db.flush()
    points=[
      CollectionPoint(name="Fort Community Welcome Point (Fictional)",district="Galle",area="Galle Fort",opening_hours="Daily 08:00–19:00",location_hint="Near the public library",contact_instructions="Ask reception for PlateBridge",storage_capability="Ambient and refrigerated"),
      CollectionPoint(name="Sunrise Volunteer Hub (Fictional)",district="Galle",area="Karapitiya",opening_hours="Mon–Sat 09:00–18:00",location_hint="Near the teaching hospital junction",contact_instructions="Use the side reception",storage_capability="Ambient only"),
    ]
    db.add_all(points); db.flush()
    foods=[
      (users[1],"Fresh bakery bread and buns","bakery","Untouched end-of-day bread and vegetable buns",24,"GREEN","AVAILABLE",2,"Wheat, milk"),
      (users[0],"Rice and curry portions","cooked_meal","Rice, dhal, beans and coconut sambol",8,"AMBER","PENDING_COORDINATOR_REVIEW",1,"Coconut"),
      (users[7],"Vegetable fried rice","cooked_meal","Canteen surplus separated before service",18,"AMBER","AVAILABLE",2,"Soy, egg"),
      (users[6],"Ripe bananas","whole_produce","Whole fruit from a home garden",14,"GREEN","AVAILABLE",6,"None declared"),
      (users[1],"String hoppers","bakery","Fresh untouched string hoppers",20,"GREEN","AVAILABLE",3,"None declared"),
      (users[7],"Unopened dry rations","dry_rations","Sealed rice and dhal packs",10,"GREEN","AVAILABLE",20,"None declared"),
      (users[0],"Shared plate leftovers","cooked_meal","Food returned after serving",3,"RED","REJECTED",1,"Coconut, fish"),
      (users[1],"Coconut buns","bakery","Sealed fresh buns",12,"GREEN","COMPLETED",24,"Wheat, coconut"),
      (users[7],"Dhal and vegetable curry","cooked_meal","Refrigerated canteen batch",15,"AMBER","COMPLETED",30,"Coconut"),
      (users[1],"Wholemeal loaves","bakery","Wrapped untouched loaves",9,"GREEN","COMPLETED",48,"Wheat"),
      (users[6],"Home-grown papaya","whole_produce","Whole ripe fruit",5,"GREEN","COMPLETED",36,"None declared"),
      (users[7],"Vegetable kottu","cooked_meal","Freshly prepared canteen surplus",12,"AMBER","COMPLETED",18,"Wheat, egg, soy"),
    ]
    listings=[]
    for donor,title,cat,desc,portions,klass,status,hours,allergens in foods:
        l=FoodListing(donor_id=donor.id,title=title,category=cat,description=desc,portions=portions,available_portions=0 if status=="COMPLETED" else portions,prepared_at=now-timedelta(hours=1) if cat not in {"whole_produce","dry_rations"} else None,packaged_at=now-timedelta(minutes=45),collection_deadline=now+timedelta(hours=hours),storage_method="refrigerated" if klass=="AMBER" else "sealed ambient",refrigerated=klass=="AMBER",previously_served=klass=="RED",allergens=allergens,vegetarian="fish" not in allergens.lower(),contains_egg="egg" in allergens.lower(),contains_dairy="milk" in allergens.lower(),district=donor.district,area=donor.area,classification=klass,status=status,safety_explanation={"GREEN":"Eligible for immediate matching under the current demo rules.","AMBER":"Coordinator review is required before matching.","RED":"Not eligible for human redistribution under the demo rules."}[klass],failed_checks="Previously served" if klass=="RED" else "")
        db.add(l); listings.append(l)
    db.flush()
    rescues=[]
    for i,li in enumerate(listings[7:12]):
        r=Rescue(listing_id=li.id,recipient_id=users[2 if i%2==0 else 8].id,portions=max(1,li.portions//2),fulfilment="delivery" if i%2 else "collection",collection_point_id=points[0].id,pickup_code=f"PB{1200+i}",status="RECEIVED",volunteer_id=users[3].id if i%2 else None)
        db.add(r); rescues.append(r)
    active1=Rescue(listing_id=listings[2].id,recipient_id=users[2].id,portions=4,fulfilment="delivery",pickup_code="PB4421",status="VOLUNTEER_NEEDED")
    active2=Rescue(listing_id=listings[4].id,recipient_id=users[8].id,portions=5,fulfilment="collection",collection_point_id=points[1].id,pickup_code="PB7734",status="READY_FOR_PICKUP")
    db.add_all([active1,active2]); db.flush()
    db.add_all([
      Incident(rescue_id=rescues[0].id,reporter_id=users[2].id,category="Packaging damage",description="One paper bag tore during collection.",severity="LOW",status="RESOLVED",resolution_notes="Packaging guidance shared."),
      Incident(rescue_id=active1.id,reporter_id=users[2].id,category="Late collection",description="Delivery window needs coordinator confirmation.",severity="MEDIUM",status="OPEN"),
      Message(rescue_id=active1.id,sender_id=users[2].id,body="Please leave the package at the collection point reception."),
      Notification(user_id=users[0].id,title="Listing needs review",body="Your rice and curry listing is awaiting coordinator review."),
      Notification(user_id=users[2].id,title="Delivery requested",body="A volunteer delivery task is being matched."),
      SafetyRule(key="max_cooked_hours",value="4",description="Maximum ambient time for cooked food in this demo."),
      SafetyRule(key="default_radius_km",value="25",description="Default matching radius for nearby listings."),
    ])
    for li in listings:
        db.add(AuditEvent(entity_type="listing",entity_id=li.id,action="LISTING_CREATED",actor_id=li.donor_id,detail=f"Seeded {li.classification.lower()} demo listing"))
    db.commit(); db.close()

if __name__ == "__main__":
    reset_database()
    print("PlateBridge LK demo database reset and seeded.")

