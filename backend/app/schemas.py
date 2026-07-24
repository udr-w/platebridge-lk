from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class DemoLogin(BaseModel):
    email: str
    password: str

class ListingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=140)
    description: str = ""
    category: str
    portions: int = Field(ge=1, le=500)
    prepared_at: datetime | None = None
    packaged_at: datetime | None = None
    collection_deadline: datetime
    storage_method: str = "room_temperature"
    refrigerated: bool = False
    frozen: bool = False
    previously_served: bool = False
    partially_eaten: bool = False
    reused_utensils: bool = False
    visible_spoilage: bool = False
    damaged_packaging: bool = False
    marked_unsafe: bool = False
    ingredients: str = ""
    allergens: str = "None declared"
    vegetarian: bool = False
    vegan: bool = False
    contains_meat: bool = False
    contains_fish: bool = False
    contains_egg: bool = False
    contains_dairy: bool = False
    halal: str = "not_confirmed"
    spiciness: str = "mild"
    packaging_type: str = "sealed container"
    containers_returnable: bool = False
    district: str = "Galle"
    area: str = "Galle Fort"
    instructions: str = "Show the pickup code."
    photo_url: str | None = None

class ClaimCreate(BaseModel):
    portions: int = Field(ge=1)
    fulfilment: str = "collection"
    collection_point_id: int | None = None

class IncidentCreate(BaseModel):
    rescue_id: int
    category: str
    description: str = Field(min_length=5)
    severity: str = "MEDIUM"

class MessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=1000)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; email: str; name: str; role: str; donor_type: str | None
    organisation: str | None; district: str; area: str; language: str
    alias: str | None; anonymous: bool; active: bool

