from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ----------------- ÖĞRENCİ ŞEMALARI ----------------- #

# Temel (Ortak) Sütunlar
class OgrenciBase(BaseModel):
    ogrenci_id: int
    ad: str
    soyad: str
    bolum_id: int

# POST Isteklerinde Kullanıcıdan Alınacak Şema (Örn: sifre verisi de isteniyor)
class OgrenciCreate(OgrenciBase):
    sifre: int 

# API'nin Dışarıya Döneceği/Göstereceği Şema (Id ve Kayıt Tarihi veritabanından gelecek, şifre asla dönülmeyecek)
class OgrenciResponse(OgrenciBase):
    ogrenci_id: int
    kayit_tarihi: Optional[date] = None

    class Config:
        from_attributes = True

# Öğrenci Transkript Görüntüsü
class TranskriptResponse(BaseModel):
    Ders: Optional[str] = None
    Vize: Optional[int] = None
    Final: Optional[int] = None
    Ortalama: Optional[float] = None
    Durum: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------- DERS ŞEMALARI ----------------- #

class DersResponse(BaseModel):
    ders_id: int
    ders_adi: Optional[str] = None
    bolum_id: Optional[int] = None
    ogretmen_id: Optional[int] = None

    class Config:
        from_attributes = True

class DersBasariResponse(BaseModel):
    Ders: Optional[str] = None
    Ogrenci_Sayisi: Optional[int] = None
    Ortalama_Not: Optional[float] = None
    Basari_Orani: Optional[float] = None

    class Config:
        from_attributes = True

# ----------------- NOT ŞEMALARI ----------------- #

class NotCreate(BaseModel):
    ogrenci_id: int
    ders_id: int
    vize: Optional[int] = None
    final: Optional[int] = None

class NotUpdate(BaseModel):
    vize: Optional[int] = None
    final: Optional[int] = None

class NotResponse(BaseModel):
    not_id: int
    ogrenci_id: int
    ders_id: int
    vize: Optional[int] = None
    final: Optional[int] = None

    class Config:
        from_attributes = True

# ----------------- LOGIN ŞEMALARI (JWT) ----------------- #

class Token(BaseModel):
    access_token: str
    token_type: str
