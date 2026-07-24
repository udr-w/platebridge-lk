from datetime import datetime,timedelta
from types import SimpleNamespace
from app.safety import assess_food

def item(**kw):
    base=dict(prepared_at=datetime.utcnow()-timedelta(hours=1),collection_deadline=datetime.utcnow()+timedelta(hours=2),category="bakery",storage_method="sealed",refrigerated=False,frozen=False,partially_eaten=False,previously_served=False,visible_spoilage=False,damaged_packaging=False,marked_unsafe=False,contains_meat=False,contains_fish=False,contains_egg=False,contains_dairy=False)
    base.update(kw);return SimpleNamespace(**base)
def test_green():assert assess_food(item())["classification"]=="GREEN"
def test_amber():assert assess_food(item(category="cooked_meal"))["classification"]=="AMBER"
def test_red():assert assess_food(item(partially_eaten=True))["classification"]=="RED"

