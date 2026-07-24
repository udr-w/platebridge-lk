import os
os.environ["DATABASE_URL"]="sqlite:///./test_platebridge.db"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.seed import reset_database

@pytest.fixture(autouse=True)
def seeded():reset_database()
@pytest.fixture
def client():return TestClient(app)
@pytest.fixture
def tokens(client):
    def login(email):return client.post("/api/auth/demo-login",json={"email":email,"password":"demo123"}).json()["access_token"]
    return {r:login(e) for r,e in {"donor":"donor.home@platebridge.demo","recipient":"recipient@platebridge.demo","volunteer":"volunteer@platebridge.demo","coordinator":"coordinator@platebridge.demo","admin":"admin@platebridge.demo"}.items()}

