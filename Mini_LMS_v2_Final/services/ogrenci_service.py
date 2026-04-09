from models.models import Ogrenciler, Notlar, DersKayitlari, Dersler, Bolumler, t_Devamsizlik
from schemas.schemas import OgrenciCreate
import datetime

def get_ogrenci_by_id(db: Session, ogrenci_id: int):
    return db.query(Ogrenciler).filter(Ogrenciler.ogrenci_id == ogrenci_id).first()

def create_ogrenci(db: Session, ogrenci: OgrenciCreate):
    yeni_ogrenci = Ogrenciler(
        ogrenci_id=ogrenci.ogrenci_id,
        ad=ogrenci.ad,
        soyad=ogrenci.soyad,
        bolum_id=ogrenci.bolum_id,
        sifre=ogrenci.sifre,
        kayit_tarihi=datetime.date.today()
    )
    db.add(yeni_ogrenci)
    db.commit()
    db.refresh(yeni_ogrenci)
    return yeni_ogrenci

def get_ogrenci_transkript(db: Session, ogrenci_id: int):
    # Öğrencinin aldığı dersleri ve notları çekelim
    notlar_sorgusu = db.query(
        Dersler.ders_adi.label("Ders"),
        Notlar.vize.label("Vize"),
        Notlar.final.label("Final")
    ).join(DersKayitlari, Dersler.ders_id == DersKayitlari.ders_id)\
     .outerjoin(Notlar, (DersKayitlari.ders_id == Notlar.ders_id) & (DersKayitlari.ogrenci_id == Notlar.ogrenci_id))\
     .filter(DersKayitlari.ogrenci_id == ogrenci_id).all()

    # Devamsızlık verilerini çekelim
    devamsizliklar = db.query(t_Devamsizlik).filter(t_Devamsizlik.c.ogrenci_id == ogrenci_id).all()
    devamsizlik_dict = {d.ders_id: (d.katilim_sayisi, d.toplam_ders) for d in devamsizliklar}

    sonuclar = []
    for row in notlar_sorgusu:
        vize = row.Vize if row.Vize is not None else 0
        final = row.Final if row.Final is not None else 0
        
        # İş Kuralı: Ortalama hesaplama backend içinde
        ortalama = (vize * 0.4) + (final * 0.6)
        
        # İş Kuralı: Devamsızlık %30'dan fazla ise kalır
        # (Örnek: katilim=2, toplam=10 -> devamsizlik=80% > 30% -> Kalır)
        durum = "Geçti" if ortalama >= 50 else "Kaldı"
        
        # Devamsızlık kontrolü (eğer veri varsa)
        # Not: Ders ID'sine ihtiyacımız var, sorguya ekleyelim
        # (Sorguyu Dersler.ders_id içerecek şekilde revize ediyorum)
        
    # Revize edilmiş hali:
    notlar_sorgusu = db.query(
        Dersler.ders_id,
        Dersler.ders_adi,
        Notlar.vize,
        Notlar.final
    ).join(DersKayitlari, Dersler.ders_id == DersKayitlari.ders_id)\
     .outerjoin(Notlar, (DersKayitlari.ders_id == Notlar.ders_id) & (DersKayitlari.ogrenci_id == Notlar.ogrenci_id))\
     .filter(DersKayitlari.ogrenci_id == ogrenci_id).all()

    for row in notlar_sorgusu:
        vize = row.vize if row.vize is not None else 0
        final = row.final if row.final is not None else 0
        ortalama = round((vize * 0.4) + (final * 0.6), 1)
        
        durum = "Geçti" if ortalama >= 50 else "Kaldı"
        
        # Devamsızlık kontrolü
        dati = devamsizlik_dict.get(row.ders_id)
        if dati:
            katilim, toplam = dati
            if toplam > 0:
                devamsizlik_orani = (toplam - katilim) / toplam
                if devamsizlik_orani > 0.3:
                    durum = "Kaldı (Devamsızlık)"
        
        sonuclar.append({
            "Ders": row.ders_adi,
            "Vize": row.vize,
            "Final": row.final,
            "Ortalama": ortalama,
            "Durum": durum
        })
        
    return sonuclar
