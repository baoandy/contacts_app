from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app import schemas
from app.utils import check_duplicate_email
from app.exceptions import DuplicateEmailError
from app.websocket_connection_manager import manager
import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/contacts", response_model=list[schemas.ContactOut])
def get_contacts_for_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        contacts = db.query(models.Contact).filter(
            models.Contact.user_id == user_id
        ).all()
        
        return contacts
    except Exception as e:
        db.rollback()
        raise