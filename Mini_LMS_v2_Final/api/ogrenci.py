from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services import ogrenci_service
from schemas.schemas import OgrenciResponse, OgrenciCreate, TranskriptResponse

from core.security import get_current_user

router = APIRouter(
    prefix="/ogrenci",
    tags=["Student"]
)

@router.get("/{id}", response_model=OgrenciResponse)
def get_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # İş Kuralı: Öğrenci sadece kendi bilgilerini görebilir
    if current_user.get("role") == "ogrenci" and int(current_user.get("sub")) != id:
        raise HTTPException(status_code=403, detail="Sadece kendi bilgilerinize erişebilirsiniz")
        
    student = ogrenci_service.get_ogrenci_by_id(db, ogrenci_id=id)
    if not student:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    return student

@router.post("", response_model=OgrenciResponse, status_code=status.HTTP_201_CREATED)
def add_student(ogrenci: OgrenciCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # İş Kuralı: Sadece öğretmen/admin öğrenci ekleyebilir
    if current_user.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Öğrenci ekleme yetkiniz yok")
        
    try:
        return ogrenci_service.create_ogrenci(db, ogrenci)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}/transkript", response_model=List[TranskriptResponse])
def get_transcript(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # İş Kuralı: Öğrenci sadece kendi transkriptini görebilir
    if current_user.get("role") == "ogrenci" and int(current_user.get("sub")) != id:
        raise HTTPException(status_code=403, detail="Sadece kendi transkriptinize erişebilirsiniz")

    student = ogrenci_service.get_ogrenci_by_id(db, id)
    if not student:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
        
    return ogrenci_service.get_ogrenci_transkript(db, ogrenci_id=id)
