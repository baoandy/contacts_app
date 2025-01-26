from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re

def validate_phone(v: str) -> str:
    """Validate phone number format."""
    digits = re.sub(r'\D', '', v)
    if not (10 <= len(digits) <= 15):
        raise ValueError("Phone number must contain between 10 and 15 digits")
    return v

def validate_name(v: str) -> str:
    """Validate name format."""
    if not re.match(r"^[A-Za-z\s\-']+$", v):
        raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
    return v

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[A-Za-z\s\-']+$", v):
            raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r'\D', '', v)
        if not (10 <= len(digits) <= 15):
            raise ValueError("Phone number must contain between 10 and 15 digits")
        return v

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserSimple(UserBase):
    id: int
    class Config:
        orm_mode = True

class ContactVersionOut(ContactBase):
    id: int
    contact_id: int
    created_at: datetime
    modified_by: UserSimple
    class Config:
        orm_mode = True

class ContactOut(BaseModel):
    id: int
    current_version: Optional[ContactVersionOut] = None
    versions: List[ContactVersionOut] = []
    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    contacts: List[ContactOut] = []
    class Config:
        orm_mode = True 