from sqlalchemy.orm import Session
from app.db import models
from phonenumbers import parse, is_valid_number, NumberParseException

def check_duplicate_email(db: Session, email: str, exclude_contact_id: int | None = None) -> bool:
    """Check if a contact with the given email already exists.
    
    Args:
        db: Database session
        email: Email to check
        exclude_contact_id: Optional contact ID to exclude from the check (used for updates)
        
    Returns:
        True if a duplicate exists, False otherwise
    """
    query = (
        db.query(models.Contact)
        .join(models.ContactVersion)
        .filter(models.ContactVersion.email == email)
    )
    
    if exclude_contact_id is not None:
        query = query.filter(models.Contact.id != exclude_contact_id)
        
    result = db.query(query.exists()).scalar()
    print(f"\n\n\n DEBUGGING RESULT {result} \n\n\n")
    return result

def check_valid_phone_number(phone_number: str) -> bool:
    try:
        parsed_number = parse(phone_number, "US")
        return is_valid_number(parsed_number)
    except NumberParseException:
        return False