from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import PRODUCT_NAME
from .database import Base,SessionLocal,engine
from .models import User
from .seed import reset_database
from .routes import auth,core,listings,rescues

app=FastAPI(title=f"{PRODUCT_NAME} API",version="0.1.0",description="Prototype food-rescue coordination API. Automated checks do not certify food safety.")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:8080"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router,prefix="/api")
app.include_router(listings.router,prefix="/api")
app.include_router(rescues.router,prefix="/api")
app.include_router(core.router,prefix="/api")
@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        needs_seed=db.query(User).count()==0
    if needs_seed:reset_database()
@app.get("/health")
def health():return {"status":"ok","service":PRODUCT_NAME}
