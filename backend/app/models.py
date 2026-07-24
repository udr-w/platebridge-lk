from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(30), index=True)
    donor_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    organisation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    district: Mapped[str] = mapped_column(String(50), default="Galle")
    area: Mapped[str] = mapped_column(String(80), default="Galle Fort")
    language: Mapped[str] = mapped_column(String(5), default="en")
    alias: Mapped[str | None] = mapped_column(String(80), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    latitude: Mapped[float] = mapped_column(Float, default=6.0329)
    longitude: Mapped[float] = mapped_column(Float, default=80.2168)

class FoodListing(Base):
    __tablename__ = "food_listings"
    id: Mapped[int] = mapped_column(primary_key=True)
    donor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(140))
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(60))
    portions: Mapped[int] = mapped_column(Integer)
    available_portions: Mapped[int] = mapped_column(Integer)
    prepared_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    packaged_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    collection_deadline: Mapped[datetime] = mapped_column(DateTime)
    storage_method: Mapped[str] = mapped_column(String(40), default="room_temperature")
    refrigerated: Mapped[bool] = mapped_column(Boolean, default=False)
    frozen: Mapped[bool] = mapped_column(Boolean, default=False)
    previously_served: Mapped[bool] = mapped_column(Boolean, default=False)
    partially_eaten: Mapped[bool] = mapped_column(Boolean, default=False)
    reused_utensils: Mapped[bool] = mapped_column(Boolean, default=False)
    visible_spoilage: Mapped[bool] = mapped_column(Boolean, default=False)
    damaged_packaging: Mapped[bool] = mapped_column(Boolean, default=False)
    marked_unsafe: Mapped[bool] = mapped_column(Boolean, default=False)
    ingredients: Mapped[str] = mapped_column(Text, default="")
    allergens: Mapped[str] = mapped_column(String(240), default="None declared")
    vegetarian: Mapped[bool] = mapped_column(Boolean, default=False)
    vegan: Mapped[bool] = mapped_column(Boolean, default=False)
    contains_meat: Mapped[bool] = mapped_column(Boolean, default=False)
    contains_fish: Mapped[bool] = mapped_column(Boolean, default=False)
    contains_egg: Mapped[bool] = mapped_column(Boolean, default=False)
    contains_dairy: Mapped[bool] = mapped_column(Boolean, default=False)
    halal: Mapped[str] = mapped_column(String(30), default="not_confirmed")
    spiciness: Mapped[str] = mapped_column(String(20), default="mild")
    packaging_type: Mapped[str] = mapped_column(String(60), default="sealed container")
    containers_returnable: Mapped[bool] = mapped_column(Boolean, default=False)
    district: Mapped[str] = mapped_column(String(50), default="Galle")
    area: Mapped[str] = mapped_column(String(80), default="Galle Fort")
    latitude: Mapped[float] = mapped_column(Float, default=6.0329)
    longitude: Mapped[float] = mapped_column(Float, default=80.2168)
    instructions: Mapped[str] = mapped_column(Text, default="Show the pickup code.")
    photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    classification: Mapped[str] = mapped_column(String(10), default="AMBER")
    safety_explanation: Mapped[str] = mapped_column(Text, default="Pending assessment")
    failed_checks: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="DRAFT", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    donor: Mapped[User] = relationship()

class Rescue(Base):
    __tablename__ = "rescues"
    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("food_listings.id"), index=True)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    portions: Mapped[int] = mapped_column(Integer)
    fulfilment: Mapped[str] = mapped_column(String(30), default="collection")
    collection_point_id: Mapped[int | None] = mapped_column(ForeignKey("collection_points.id"), nullable=True)
    pickup_code: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(40), default="CONFIRMED", index=True)
    volunteer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    listing: Mapped[FoodListing] = relationship()
    recipient: Mapped[User] = relationship(foreign_keys=[recipient_id])
    volunteer: Mapped[User | None] = relationship(foreign_keys=[volunteer_id])

class CollectionPoint(Base):
    __tablename__ = "collection_points"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    district: Mapped[str] = mapped_column(String(50))
    area: Mapped[str] = mapped_column(String(80))
    opening_hours: Mapped[str] = mapped_column(String(120))
    location_hint: Mapped[str] = mapped_column(String(160))
    contact_instructions: Mapped[str] = mapped_column(String(160))
    storage_capability: Mapped[str] = mapped_column(String(80))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(primary_key=True)
    rescue_id: Mapped[int] = mapped_column(ForeignKey("rescues.id"), index=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), default="MEDIUM")
    status: Mapped[str] = mapped_column(String(30), default="OPEN")
    coordinator_notes: Mapped[str] = mapped_column(Text, default="")
    resolution_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(30), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(80))
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    rescue_id: Mapped[int] = mapped_column(ForeignKey("rescues.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(140))
    body: Mapped[str] = mapped_column(Text)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SafetyRule(Base):
    __tablename__ = "safety_rules"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(80), unique=True)
    value: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)

