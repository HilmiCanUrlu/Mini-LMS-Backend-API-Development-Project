from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import ogrenci_service
from app.schemas.schemas import OgrenciResponse, OgrenciCreate

# API Endpoint'lerinin yollarını bağladığımız Router (Örn: localhost:8000/ogrenci/..)
router = APIRouter(
    prefix="/ogrenci",
    tags=["Öğrenci İşlemleri"]
)

@router.get("/{id}", response_model=OgrenciResponse, summary="ID ile Öğrenciyi Bul")
def ogrenci_bilgisi_getir(id: int, db: Session = Depends(get_db)):
    """
    Veritabanından ID değerine göre bir öğrencinin tüm bilgilerini çeker.
    """
    # 1. İş kuralımız (Service) üzerinden veritabanına bağlan
    ogrenci = ogrenci_service.get_ogrenci_by_id(db, ogrenci_id=id)
    
    # 2. Hata Yakalama (Exception Handling): Bulunamazsa 404 dön
    if ogrenci is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{id} numaralı öğrenci sistemde kayıtlı değil!"
        )
    
    # Başarılıysa şema üzerinden dönecek (Şifreyi gizleyip sadece ogrenci_id, ad, soyad döner)
    return ogrenci


@router.post("", response_model=OgrenciResponse, status_code=status.HTTP_201_CREATED, summary="Sisteme Yenı Öğrenci Ekle (Kayıt Ol)")
def ogrenci_ekle(ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    """
    Dışarıdan (Kullanıcıdan) JSON olarak gelen yeni öğrenci bilgilerini (şifre vs.)
    veritabanına kaydeder ve şifreyi gizleyerek başarı yanıtı döner.
    """
    try:
        yeni_kayit = ogrenci_service.create_ogrenci(db, ogrenci)
        return yeni_kayit
    except Exception as e:
        # Örn: bolum_id geçersizse SQLAlchemy veritabanı kısıtlamasına takılıp hata fırlatabilir.
        raise HTTPException(
            status_code=500, 
            detail=f"Öğrenci eklenirken bir hata oluştu. Muhtemelen bolum_id mevcut değil: {str(e)}"
        )

from typing import List
from app.schemas.schemas import TranskriptResponse

@router.get("/{id}/transkript", response_model=List[TranskriptResponse], summary="Öğrencinin Transkriptini (Notlarını) Getir")
def ogrenci_transkript_getir(id: int, db: Session = Depends(get_db)):
    """
    Belirli bir öğrencinin aldığı dersleri, vize/final notlarını, 
    ortalamasını ve başarı durumunu getirir. Öğrencinin var olup olmadığı da kontrol edilir.
    """
    ogrenci = ogrenci_service.get_ogrenci_by_id(db, id)
    if not ogrenci:
        raise HTTPException(status_code=404, detail=f"{id} numaralı öğrenci sistemde bulunamadı!")
        
    transkript_listesi = ogrenci_service.get_ogrenci_transkript(db, ogrenci_id=id)
    return transkript_listesi
