from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import engine, get_db
import app.models.models as models

# Veritabanı tablolarının motor ile eşleştiğinden emin olmak için (Hazır veritabanı olduğu için tablolar yeniden oluşturulmayacak, sadece uyumlanacak)
# models.Base.metadata.create_all(bind=engine) -> Veritabanımız zaten dolu olduğu için bu adımı atlıyoruz.

from fastapi.middleware.cors import CORSMiddleware

# FastAPI Uvegilamamızın Başlangıç Noktası (Ana Sınıf)
app = FastAPI(
    title="Mini LMS Backend API",
    description="Öğrenci, Ders ve Not otomasyon sistemi API Arayüzü",
    version="1.0.0"
)

# CORS Korumasını (Güvenlik Kalkanını) İsteğe Göre Ayarlama Modülü
# İleride bir React/HTML önyüzü (Frontend) yazdığımızda engellenmemesi için gereklidir!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Her türlü web sayfasına izin veriyoruz.
    allow_credentials=True,
    allow_methods=["*"], # Bütün HTTP metodlarına (GET, POST vs)
    allow_headers=["*"], 
)

# Kök (Root) Endpoint: API'nin çalışıp çalışmadığını kontrol eder.
@app.get("/", tags=["Sistem"])
def ana_sayfa():
    return {
        "mesaj": "Mini LMS API Başarıyla Çalışıyor! 🎉",
        "swagger_dokuman": "API Dokümantasyonu için tarayıcınızdan /docs adresine gidin."
    }

# Veritabanı Test Endpointi: SQL Server'a sağlıklı bağlanılıp bağlanılamadığını test eder.
@app.get("/db-test", tags=["Sistem"])
def veritabani_baglanti_testi(db: Session = Depends(get_db)):
    try:
        # SQL Server'a basit bir 'SELECT 1' sorgusu atıyoruz
        sonuc = db.execute(text("SELECT 1")).scalar()
        if sonuc == 1:
            return {"durum": "BAŞARILI", "mesaj": "SQL Server (obs) veritabanına bağlantı mükemmel şekilde sağlandı! 🚀"}
    except Exception as e:
        return {"durum": "HATA", "mesaj": "Veritabanı bağlantısı sırasında bir hata oluştu.", "hata_detayi": str(e)}

# ROUTER BAĞLANTILARI
# Her yazdığımız yeni API servisini bir nevi sunucuya entegre ediyoruz (Tak-Çalıştır)
from app.api import auth, ogrenci, ders, notlar
# Auth Router'ını En Başta Yüklüyoruz (Swagger Kilit İşareti için login rotasını besler)
app.include_router(auth.router)
app.include_router(ogrenci.router)
app.include_router(ders.router)
app.include_router(notlar.router)
