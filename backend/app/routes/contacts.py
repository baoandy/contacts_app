import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db import models
from app.db.database import get_db
from app import schemas
from app.utils import check_duplicate_email
from app.exceptions import DuplicateEmailError
from app.websocket_connection_manager import manager
import datetime

SERVER_LAG_TIME_SECONDS = 5

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("", response_model=list[schemas.ContactOut])
def get_all_contacts(db: Session = Depends(get_db)):
    try:
        contacts = db.query(models.Contact).all()
        return contacts
    except Exception as e:
        db.rollback()
        raise

@router.post("/{user_id}", response_model=schemas.ContactOut)
async def create_contact(user_id: int, contact: schemas.ContactBase, db: Session = Depends(get_db)):
    try:
        time.sleep(SERVER_LAG_TIME_SECONDS)
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if check_duplicate_email(db, contact.email):
            raise DuplicateEmailError()

        new_contact = models.Contact(user_id=user.id)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        contact_version = models.ContactVersion(
            contact_id=new_contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            modified_by_id=user.id,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(contact_version)
        db.commit()
        db.refresh(new_contact)

        await manager.broadcast_create_contact(new_contact, user)
        return new_contact
    except Exception as e:
        db.rollback()
        raise

@router.put("/{contact_id}", response_model=schemas.ContactOut)
async def update_contact(
    contact_id: int,
    contact: schemas.ContactBase,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        time.sleep(SERVER_LAG_TIME_SECONDS)
        if user_id is None:
            user_id = 1  # Default to demo user if not provided
        
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not db_contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        if check_duplicate_email(db, contact.email, exclude_contact_id=contact_id):
            raise DuplicateEmailError()

        contact_version = models.ContactVersion(
            contact_id=db_contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            modified_by_id=user_id,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(contact_version)
        db.commit()
        db.refresh(db_contact)
        await manager.broadcast_update_contact(contact_version, user)
        return db_contact
    except Exception as e:
        db.rollback()
        raise

@router.get("/{contact_id}/versions", response_model=list[schemas.ContactVersionOut])
def get_contact_versions(contact_id: int, db: Session = Depends(get_db)):
    try:
        contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        versions = db.query(models.ContactVersion).filter(
            models.ContactVersion.contact_id == contact_id
        ).order_by(models.ContactVersion.created_at.desc()).all()
        
        return versions
    except Exception as e:
        db.rollback()
        raise

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        # Store contact info for websocket notification before deletion
        contact_id = contact.id
        first_name = contact.current_version.first_name
        last_name = contact.current_version.last_name

        # Delete all versions first (due to foreign key constraint)
        db.query(models.ContactVersion).filter(models.ContactVersion.contact_id == contact_id).delete()
        db.query(models.Contact).filter(models.Contact.id == contact_id).delete()
        
        db.commit()

        await manager.broadcast_delete_contact(contact_id, first_name, last_name, user)
        return {"message": "Contact deleted successfully"}
    except Exception as e:
        db.rollback()
        raise

@router.get("/check-email-exists/{email}")
def check_email_exists(email: str, db: Session = Depends(lambda: get_db(no_cache=True))):
    try:
        exists = check_duplicate_email(db, email)
        response = {"exists": exists}
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return JSONResponse(content=response, headers=headers)
    except Exception as e:
        db.rollback()
        raise