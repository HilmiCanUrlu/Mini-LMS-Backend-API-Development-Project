from sqlalchemy.orm import Session
from app.models.models import Notlar, DersKayitlari, t_Devamsizlik
from app.schemas.schemas import NotCreate, NotUpdate
from fastapi import HTTPException

def check_ogrenci_derse_kayitlimi(db: Session, ogrenci_id: int, ders_id: int):
    # Kural 1: Öğrenci Derse Kayıtlı Olmak Zorunda
    kayit = db.query(DersKayitlari).filter(
        DersKayitlari.ogrenci_id == ogrenci_id,
        DersKayitlari.ders_id == ders_id
    ).first()
    return kayit is not None

def check_devamsizlik_basarisizligi(db: Session, ogrenci_id: int, ders_id: int):
    # Kural 4: Devamsızlık %30'dan fazlaysa not girilemez veya otomatik başarısız sayılır
    devamsizlik_durumu = db.query(t_Devamsizlik).filter(
        t_Devamsizlik.c.ogrenci_id == ogrenci_id,
        t_Devamsizlik.c.ders_id == ders_id
    ).first()
    # Eğer devamsızlık durumu "Kaldı" içeren bir ibareyeyse
    if devamsizlik_durumu and devamsizlik_durumu.durum == 'Devamsizliktan Kaldi':
        return True
    return False

def get_not_by_ogrenci_ve_ders(db: Session, ogrenci_id: int, ders_id: int):
    return db.query(Notlar).filter(
        Notlar.ogrenci_id == ogrenci_id,
        Notlar.ders_id == ders_id
    ).first()

def validate_not_sinirlari(vize: int = None, final: int = None):
    # Kural 3: Not aralığı 0-100 olmalıdır.
    if vize is not None and not (0 <= vize <= 100):
        raise HTTPException(status_code=400, detail="Vize notu 0 ile 100 arasında olmalıdır!")
    if final is not None and not (0 <= final <= 100):
        raise HTTPException(status_code=400, detail="Final notu 0 ile 100 arasında olmalıdır!")

def create_not(db: Session, not_data: NotCreate):
    validate_not_sinirlari(not_data.vize, not_data.final)
    
    if not check_ogrenci_derse_kayitlimi(db, not_data.ogrenci_id, not_data.ders_id):
        raise HTTPException(status_code=400, detail="Kurallar İhlali: Öğrenci bu derse kayıtlı değil! Not girilemez.")
        
    if check_devamsizlik_basarisizligi(db, not_data.ogrenci_id, not_data.ders_id):
         raise HTTPException(status_code=400, detail="Kurallar İhlali: Öğrenci bu dersten devamsızlıktan kalmış! Not girilemez.")
    
    # Kural 2: Aynı ders için ancak BİR defa not giriş kaydı açılır (Sonrakiler PUT ile güncellenir)
    eski_not = get_not_by_ogrenci_ve_ders(db, not_data.ogrenci_id, not_data.ders_id)
    if eski_not:
        raise HTTPException(status_code=400, detail="Öğrencinin bu ders için zaten not kaydı var. Lütfen Güncelleme (PUT) işlemini kullanın.")

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
    validate_not_sinirlari(update_data.vize, update_data.final)
    kayitli_not = db.query(Notlar).filter(Notlar.not_id == not_id).first()
    if not kayitli_not:
        raise HTTPException(status_code=404, detail="Sistemde böyle bir not bulunamadı!")
    
    if update_data.vize is not None:
        kayitli_not.vize = update_data.vize
    if update_data.final is not None:
        kayitli_not.final = update_data.final
        
    db.commit()
    db.refresh(kayitli_not)
    return kayitli_not
