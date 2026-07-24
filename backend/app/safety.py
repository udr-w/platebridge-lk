from datetime import datetime
from .config import MAX_COOKED_HOURS

def assess_food(data, now: datetime | None = None):
    now = now or datetime.utcnow()
    failed = []
    if not data.prepared_at and data.category not in {"dry_rations", "whole_produce", "packaged"}:
        failed.append("Preparation time is unknown")
    if data.partially_eaten:
        failed.append("Food has been partially eaten")
    if data.previously_served:
        failed.append("Food was previously served")
    if data.visible_spoilage:
        failed.append("Visible spoilage was reported")
    if data.damaged_packaging:
        failed.append("Packaging is damaged or leaking")
    if data.marked_unsafe:
        failed.append("Donor marked the food unsafe")
    if data.collection_deadline.timestamp() <= now.timestamp():
        failed.append("Collection deadline has passed")
    if data.prepared_at and now.timestamp() - data.prepared_at.timestamp() > MAX_COOKED_HOURS * 3600 and not (data.refrigerated or data.frozen):
        failed.append(f"Cooked food exceeded the {MAX_COOKED_HOURS}-hour demo limit without cold storage")
    if failed:
        return {"classification":"RED", "explanation":"Not eligible for human redistribution under the demo rules.", "failed_checks":failed}
    amber = []
    if any((data.contains_meat, data.contains_fish, data.contains_egg, data.contains_dairy)):
        amber.append("Contains a higher-risk ingredient")
    if data.refrigerated or data.frozen:
        amber.append("Cold-chain handling needs confirmation")
    if data.category in {"cooked_meal", "event_food"}:
        amber.append("Prepared meals require coordinator review")
    if not data.storage_method:
        amber.append("Storage information is incomplete")
    if amber:
        return {"classification":"AMBER", "explanation":"Coordinator review is required before matching.", "failed_checks":amber}
    return {"classification":"GREEN", "explanation":"Eligible for immediate matching under the current demo rules.", "failed_checks":[]}
