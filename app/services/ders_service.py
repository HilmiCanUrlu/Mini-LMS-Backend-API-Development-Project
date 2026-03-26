from sqlalchemy.orm import Session
from app.models.models import Dersler, t_vw_Ders_Analiz

def get_ders_by_id(db: Session, ders_id: int):
    """
    Veritabanında ders tablosundan primary key'e göre eşleşen tek dersi döndürür.
    """
    return db.query(Dersler).filter(Dersler.ders_id == ders_id).first()

def get_ders_basari(db: Session, ders_id: int):
    """
    SQL Server'daki 'vw_Ders_Analiz' View'ından dersin adıyla eşleşen 
    istatistikleri çeker. Bu veri veritabanında t_vw nesnesi olduğu için Dict döndürürüz.
    """
    ders = get_ders_by_id(db, ders_id)
    if not ders or not ders.ders_adi:
        return None
        
    # View, ders id'sini değil adını saklıyordu, bu yüzden ada göre SQL WHERE yazıyoruz
    basari = db.query(t_vw_Ders_Analiz).filter(t_vw_Ders_Analiz.c.Ders == ders.ders_adi).first()
    return dict(basari._mapping) if basari else None
