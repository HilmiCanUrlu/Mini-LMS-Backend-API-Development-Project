from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import ders_service
from app.schemas.schemas import DersResponse, DersBasariResponse

router = APIRouter(
    prefix="/ders",
    tags=["Ders İşlemleri"]
)

@router.get("/{id}", response_model=DersResponse, summary="ID ile Dersin Bilgisini Getir")
def ders_bilgisi_getir(id: int, db: Session = Depends(get_db)):
    """
    Kullanıcının girdiği dersin temel bilgilerini (ders adı, öğretmeni vb.) çeker.
    """
    ders = ders_service.get_ders_by_id(db, ders_id=id)
    if ders is None:
        raise HTTPException(status_code=404, detail=f"Sistemde id'si {id} olan ders bulunamadı!")
    return ders

@router.get("/{id}/basari", response_model=DersBasariResponse, summary="Dersin Genel Başarı Raporunu Çek")
def ders_basari_getir(id: int, db: Session = Depends(get_db)):
    """
    İlgili dersin analitiğini getirir. SQL Server tarafından View (vw_Ders_Analiz) ile 
    önceden hesaplanmış olan; öğrenci sayısı, sınıf ortalaması ve başarı oranı döner.
    """
    ders = ders_service.get_ders_by_id(db, ders_id=id)
    if ders is None:
        raise HTTPException(status_code=404, detail="Önce dersin kendisi bulunmalı!")

    basari = ders_service.get_ders_basari(db, ders_id=id)
    if basari is None:
         raise HTTPException(status_code=404, detail="Bu ders için henüz not girilmiş bir öğrenci olmadığı için analiz verisi yok.")
         
    return basari
