from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.models import Ogrenciler, Kullanicilar
from app.schemas.schemas import Token

router = APIRouter(
    tags=["1. Kimlik Doğrulama (Login)"] # Swagger Listesinde En Üste Çıkacak
)

@router.post("/login", response_model=Token, summary="Sisteme Giriş Yap (JWT Anahtarı Al)")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Sisteme Giriş (Login) Bölümü!
    Hem Öğretmenler hem Öğrenciler buradan giriş yapabilirler.
    Swagger UI'deki yeşil **"Authorize"** kilidine tıkladığınızda bu endpoint çalışır.
    
    Öğrenci ise -> username = 20261010
    Öğretmen ise -> username = mustafa.hoca
    """
    user_input = form_data.username
    password = form_data.password
    
    # SENARYO 1: ÖĞRENCİ GİRİŞİ (ID Rakam mı diye bakarız)
    if user_input.isdigit():
        ogrenci_id = int(user_input)
        # Veritabanında Öğrenci ara
        ogrenci = db.query(Ogrenciler).filter(Ogrenciler.ogrenci_id == ogrenci_id).first()
        
        # Eğer Öğrenci varsa ve Şifre (Örn: 12345) Eşleşiyorsa:
        if ogrenci and verify_password(password, ogrenci.sifre):
            token_data = {
                "sub": str(ogrenci.ogrenci_id), 
                "role": "ogrenci", 
                "name": f"{ogrenci.ad} {ogrenci.soyad}"
            }
            # Şifrelenmiş dijital bir davetiye yarat ve teslim et
            access_token = create_access_token(token_data)
            return {"access_token": access_token, "token_type": "bearer"}

    # SENARYO 2: ÖĞRETMEN (KULLANICI) GİRİŞİ 
    # Öğretmenler "Kullanicilar" tablosundadır.
    ogretmen = db.query(Kullanicilar).filter(Kullanicilar.kullanici_adi == user_input).first()
    
    if ogretmen and verify_password(password, ogretmen.sifre):
        token_data = {
            "sub": str(ogretmen.ogretmen_id), 
            "role": "ogretmen", 
            "name": str(ogretmen.kullanici_adi)
        }
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}

    # Hem Öğrenci Değil Hem de Öğretmen (Hatalı Şifre)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kullanıcı adı/Numarası veya şifre hatalı! Lütfen tekrar deneyiniz.",
        headers={"WWW-Authenticate": "Bearer"},
    )
