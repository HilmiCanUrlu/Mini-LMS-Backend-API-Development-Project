from sqlalchemy.orm import Session
from app.models.models import Ogrenciler
from app.schemas.schemas import OgrenciCreate
import datetime

def get_ogrenci_by_id(db: Session, ogrenci_id: int):
    """
    Veritabanında ogrenci_id kolonuna göre SqlAlchemy sorgusu gönderilir 
    ve eşleşen İLK kaydı (.first()) dizi değil, nesne olarak getirir.
    """
    return db.query(Ogrenciler).filter(Ogrenciler.ogrenci_id == ogrenci_id).first()

def create_ogrenci(db: Session, ogrenci: OgrenciCreate):
    """
    API'den (Pydantic şeması) gelen öğrenci verisini alıp 
    SQLAlchemy modeline çevirir ve veritabanına INSERT atar.
    """
    yeni_ogrenci = Ogrenciler(
        ogrenci_id=ogrenci.ogrenci_id,
        ad=ogrenci.ad,
        soyad=ogrenci.soyad,
        bolum_id=ogrenci.bolum_id,
        sifre=ogrenci.sifre,
        kayit_tarihi=datetime.date.today()
    )
    
    db.add(yeni_ogrenci) # Kaydı hafızaya ekle
    db.commit()          # Veritabanına işlemi uygula (INSERT)
    db.refresh(yeni_ogrenci) # Oluşan otomatik ID vb alanları modelde güncelle
    
    return yeni_ogrenci

from app.models.models import t_vw_TranskriptSenaryosu2

def get_ogrenci_transkript(db: Session, ogrenci_id: int):
    """
    Öğrencinin transkriptini, veritabanındaki hazır "vw_TranskriptSenaryosu2" görünümünden çeker.
    Eğer view kullanımı kısıtlıysa doğrudan modeller arası join ile de yazılabilir, 
    ancak hazır t_vw nesnesi çok daha hızlıdır!
    """
    kayitlar = db.query(t_vw_TranskriptSenaryosu2).filter(t_vw_TranskriptSenaryosu2.c.Ogrenci_Numarası == ogrenci_id).all()
    # Pydantic şemasının algılaması için dict nesnesine çeviriyoruz
    return [dict(row._mapping) for row in kayitlar]
