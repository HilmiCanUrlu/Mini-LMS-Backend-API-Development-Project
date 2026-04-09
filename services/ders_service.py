from sqlalchemy.orm import Session
from models.models import Dersler, t_vw_Ders_Analiz

def get_all_dersler(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dersler).offset(skip).limit(limit).all()

def get_ders_by_id(db: Session, ders_id: int):
    return db.query(Dersler).filter(Dersler.ders_id == ders_id).first()

def get_ders_analiz(db: Session):
    analiz_verileri = db.query(t_vw_Ders_Analiz).all()
    return [dict(satir._mapping) for satir in analiz_verileri]

def get_ders_basari_by_id(db: Session, ders_id: int):
    # Bu view ders adına göre sorgu yapıyor, o yüzden önce dersi bulmalıyız
    ders = get_ders_by_id(db, ders_id)
    if not ders:
        return None
    return db.query(t_vw_Ders_Analiz).filter(t_vw_Ders_Analiz.c.Ders == ders.ders_adi).first()
