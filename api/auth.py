from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verify_password, create_access_token
from models.models import Ogrenciler, Kullanicilar
from schemas.schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_input = form_data.username
    password = form_data.password
    
    # Check if student
    if user_input.isdigit():
        ogrenci_id = int(user_input)
        ogrenci = db.query(Ogrenciler).filter(Ogrenciler.ogrenci_id == ogrenci_id).first()
        
        if ogrenci and verify_password(password, ogrenci.sifre):
            token_data = {
                "sub": str(ogrenci.ogrenci_id), 
                "role": "ogrenci", 
                "name": f"{ogrenci.ad} {ogrenci.soyad}"
            }
            access_token = create_access_token(token_data)
            return {"access_token": access_token, "token_type": "bearer"}

    # Check if admin/teacher
    ogretmen = db.query(Kullanicilar).filter(Kullanicilar.kullanici_adi == user_input).first()
    if ogretmen and verify_password(password, ogretmen.sifre):
        token_data = {
            "sub": str(ogretmen.ogretmen_id), 
            "role": "ogretmen", 
            "name": str(ogretmen.kullanici_adi)
        }
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
