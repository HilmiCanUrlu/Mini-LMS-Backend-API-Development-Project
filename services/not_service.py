from sqlalchemy.orm import Session
from models.models import Notlar, DersKayitlari
from schemas.schemas import NotCreate, NotUpdate
from fastapi import HTTPException

def create_not(db: Session, not_data: NotCreate):
    # 1. Kayıt kontrolü
    kayit = db.query(DersKayitlari).filter(
        DersKayitlari.ogrenci_id == not_data.ogrenci_id,
        DersKayitlari.ders_id == not_data.ders_id
    ).first()
    
    if not kayit:
        raise HTTPException(status_code=400, detail="Öğrenci bu derse kayıtlı değil")

    # 2. Mükerrer kayıt kontrolü (İş Kuralı)
    mevcut_not = db.query(Notlar).filter(
        Notlar.ogrenci_id == not_data.ogrenci_id,
        Notlar.ders_id == not_data.ders_id
    ).first()
    
    if mevcut_not:
        raise HTTPException(status_code=400, detail="Bu öğrenci ve ders için zaten bir not kaydı mevcut")

    # 3. Not oluşturma
    yeni_not = Notlar(
        ogrenci_id=not_data.ogrenci_id,
        ders_id=not_data.ders_id,
        vize=not_data.vize,
        final=not_data.final
    )
    db.add(yeni_not)
    db.commit()
    db.refresh(yeni_not)
    return yeni_not

def update_not(db: Session, not_id: int, update_data: NotUpdate):
    db_not = db.query(Notlar).filter(Notlar.not_id == not_id).first()
    if not db_not:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    if update_data.vize is not None:
        db_not.vize = update_data.vize
    if update_data.final is not None:
        db_not.final = update_data.final
        
    db.commit()
    db.refresh(db_not)
    return db_not
