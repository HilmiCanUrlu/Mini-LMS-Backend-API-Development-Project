from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services import not_service
from app.schemas.schemas import NotCreate, NotUpdate, NotResponse

router = APIRouter(
    prefix="/not",
    tags=["Not İşlemleri"]
)

@router.post("", response_model=NotResponse, summary="Yeni Not Girişi Yap (Kısıtlamalı, Sadece Yetkililer)")
def not_girisi_yap(not_data: NotCreate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    """
    **DİKKAT KİLİTLİ ALAN! (JWT GEREKLİ)**
    Öğretmenlerin bir öğrenciye ilk defa vize/final notu girmesini sağlar.
    Özel Kısıtlamalar: Modeli derse kayıtlı olmayan, devamsızlıktan kalan öğrencilere not girilemez.
    0-100 kısıtlaması aralığı bulunur.
    """
    # İleri düzey doğrulama: token["role"] == "ogretmen" mi diye kontrol edebiliriz
    if token.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Sadece öğretmen yetkisi olanlar sisteme not girişi yapabilir!")
        
    return not_service.create_not(db, not_data)

@router.put("/{not_id}", response_model=NotResponse, summary="Var Olan Öğrenci Notunu Güncelle (Sadece Yetkililer)")
def not_guncelle(not_id: int, update_data: NotUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    """
    **DİKKAT KİLİTLİ ALAN! (JWT GEREKLİ)**
    Zaten not kaydı oluşturulmuş bir öğrencinin puanını günceller.
    Yine 0-100 kurallarına uyulmak zorundadır.
    """
    if token.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Sadece öğretmen yetkisi olanlar sistemde not güncelleyebilir!")

    return not_service.update_not(db, not_id=not_id, update_data=update_data)
