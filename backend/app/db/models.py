from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
from typing import Optional
from datetime import timezone

# Normally would use an authentication provider like Firebase or Supabase
# to store user information. Just for local demo purposes.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    contacts = relationship("Contact", back_populates="user")
    contact_versions = relationship("ContactVersion", back_populates="modified_by")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    versions = relationship("ContactVersion", back_populates="contact", order_by="desc(ContactVersion.created_at)")
    user = relationship("User", back_populates="contacts")
    
    @property
    def current_version(self) -> Optional["ContactVersion"]:
        return self.versions[0] if self.versions else None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "current_version": self.current_version.to_dict() if self.current_version else None,
            "versions": [v.to_dict() for v in self.versions]
        }

class ContactVersion(Base):
    __tablename__ = "contact_versions"
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True))
    modified_by_id = Column(Integer, ForeignKey("users.id"))
    
    contact = relationship("Contact", back_populates="versions")
    modified_by = relationship("User")

    def to_dict(self) -> dict:
        print("\n\n\n DEBUG ContactVersion.to_dict")
        print("Entire object:")
        print(self)
        print(f"created_at type: {type(self.created_at)}")
        print(f"created_at value: {self.created_at}")
        print(f"created_at timezone info: {self.created_at.tzinfo if self.created_at else None}")
        print("\n\n\n")
        return {
            "id": self.id,
            "contact_id": self.contact_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
            "modified_by": {
                "id": self.modified_by.id,
                "username": self.modified_by.username,
                "email": self.modified_by.email
            }
        }