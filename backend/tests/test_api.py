def auth(t):return {"Authorization":f"Bearer {t}"}
def test_login_and_metrics(client,tokens):assert client.get("/api/metrics/dashboard",headers=auth(tokens["recipient"])).status_code==200
def test_expired_listing_cannot_be_claimed(client,tokens):
    assert client.post("/api/listings/7/claim",json={"portions":1},headers=auth(tokens["recipient"])).status_code==409
def test_unavailable_portions(client,tokens):
    rows=client.get("/api/listings",headers=auth(tokens["recipient"])).json(); lid=rows[0]["id"]
    assert client.post(f"/api/listings/{lid}/claim",json={"portions":999},headers=auth(tokens["recipient"])).status_code==409
def test_anonymous_masking(client,tokens):
    rs=client.get("/api/rescues",headers=auth(tokens["donor"])).json()
    assert all("@" not in x["recipient_name"] for x in rs)
def test_volunteer_transition(client,tokens):
    task=client.get("/api/volunteer-tasks",headers=auth(tokens["volunteer"])).json()[0]
    assert client.post(f'/api/volunteer-tasks/{task["id"]}/accept',headers=auth(tokens["volunteer"])).json()["status"]=="VOLUNTEER_ASSIGNED"
def test_incident_creation(client,tokens):
    rescue=client.get("/api/rescues",headers=auth(tokens["recipient"])).json()[0]
    r=client.post("/api/incidents",json={"rescue_id":rescue["id"],"category":"Other","description":"A clear demo issue"},headers=auth(tokens["recipient"]))
    assert r.status_code==200
def test_invalid_receipt_transition(client,tokens):
    rescue=next(x for x in client.get("/api/rescues",headers=auth(tokens["recipient"])).json() if x["status"]=="VOLUNTEER_NEEDED")
    assert client.post(f'/api/rescues/{rescue["id"]}/confirm-receipt',headers=auth(tokens["recipient"])).status_code==409
def test_reset(client,tokens):assert client.post("/api/demo/reset",headers=auth(tokens["admin"])).status_code==200

