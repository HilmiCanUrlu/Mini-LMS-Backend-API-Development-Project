from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db, engine
import models.models as models
from api import auth, ogrenci, ders, notlar
from core.logging_config import setup_logging

# Initialize Logger
logger = setup_logging()
logger.info("Application starting...")

app = FastAPI(
    title="Mini LMS Backend API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["system"])
def root():
    return {
        "status": "online",
        "docs": "/docs"
    }

@app.get("/db-test", tags=["system"])
def db_test(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"status": "success", "message": "Veritabanı bağlantısı kuruldu"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

app.include_router(auth.router)
app.include_router(ogrenci.router)
app.include_router(ders.router)
app.include_router(notlar.router)
