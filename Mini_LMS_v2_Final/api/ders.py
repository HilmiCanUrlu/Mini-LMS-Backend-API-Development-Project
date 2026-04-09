from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services import ders_service
from schemas.schemas import DersResponse, DersBasariResponse

from core.security import get_current_user

router = APIRouter(
    prefix="/ders",
    tags=["Course"]
)

@router.get("", response_model=List[DersResponse])
def get_courses(db: Session = Depends(get_db)):
    return ders_service.get_all_dersler(db)

@router.get("/analiz", response_model=List[DersBasariResponse])
def get_analytics(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # İş Kuralı: Sadece öğretmen/admin tüm analizleri görebilir
    if current_user.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Analizlere erişim yetkiniz yok")
    return ders_service.get_ders_analiz(db)

@router.get("/{id}", response_model=DersResponse)
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    course = ders_service.get_ders_by_id(db, id)
    if not course:
        raise HTTPException(status_code=404, detail="Ders bulunamadı")
    return course

@router.get("/{id}/basari", response_model=DersBasariResponse)
def get_course_success(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
     # İş Kuralı: Sadece öğretmen/admin başarı analizini görebilir
    if current_user.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Ders başarı analizine erişim yetkiniz yok")
        
    success = ders_service.get_ders_basari_by_id(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Ders başarı analizi bulunamadı")
    return success
