from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from services import not_service
from schemas.schemas import NotCreate, NotUpdate, NotResponse

router = APIRouter(
    prefix="/not",
    tags=["Grade"]
)

@router.post("", response_model=NotResponse)
def create_grade(not_data: NotCreate, db: Session = Depends(get_db), token_data: dict = Depends(get_current_user)):
    if token_data.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Yetkisiz erişim")
        
    return not_service.create_not(db, not_data)

@router.put("/{id}", response_model=NotResponse)
def update_grade(id: int, update_data: NotUpdate, db: Session = Depends(get_db), token_data: dict = Depends(get_current_user)):
    if token_data.get("role") != "ogretmen":
        raise HTTPException(status_code=403, detail="Yetkisiz erişim")

    return not_service.update_not(db, not_id=id, update_data=update_data)
