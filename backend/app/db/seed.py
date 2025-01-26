from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime, timedelta, timezone
import random

# Common name components for generating plausible data
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Emily", "Andrew", "Donna", "Paul", "Michelle", "Joshua", "Laura"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
]

EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]

def generate_phone():
    """Generate a random US-format phone number"""
    area = random.randint(200, 999)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"+1 {area} {prefix} {line}"

def generate_email(first_name: str, last_name: str) -> str:
    """Generate a plausible email from a name"""
    patterns = [
        lambda f, l: f"{f.lower()}.{l.lower()}",
        lambda f, l: f"{f.lower()}{l.lower()}",
        lambda f, l: f"{f.lower()}{random.randint(1, 999)}",
        lambda f, l: f"{f[0].lower()}{l.lower()}",
        lambda f, l: f"{f.lower()}{l[0].lower()}"
    ]
    email_pattern = random.choice(patterns)(first_name, last_name)
    domain = random.choice(EMAIL_DOMAINS)
    return f"{email_pattern}@{domain}"

def generate_contact_version(contact_id: int, user_id: int, admin_id: int, base_date: datetime):
    """Generate a random contact version"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return models.ContactVersion(
        contact_id=contact_id,
        first_name=first_name,
        last_name=last_name,
        email=generate_email(first_name, last_name),
        phone=generate_phone(),
        modified_by_id=random.choice([user_id, admin_id]),
        created_at=base_date
    )

def seed_data(db: Session):
    # Create a default user if none exists
    user = db.query(models.User).first()
    if not user:
        user = models.User(
            id=1,   # for testing purposes
            username="demo_user",
            email="demo@example.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create a second user for demonstrating different modifiers
    second_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not second_user:
        second_user = models.User(
            id=2,
            username="admin_user",
            email="admin@example.com"
        )
        db.add(second_user)
        db.commit()
        db.refresh(second_user)

    # Add sample contacts if none exist
    if db.query(models.Contact).count() == 0:
        # Create 50 contacts
        contacts = [models.Contact(user_id=user.id) for _ in range(50)]
        db.add_all(contacts)
        db.commit()

        # For each contact, create 5-8 versions with random time intervals
        for contact in contacts:
            num_versions = random.randint(5, 10)
            base_date = datetime.now(timezone.utc) - timedelta(days=random.randint(90, 180))
            
            versions = []
            for i in range(num_versions):
                version = generate_contact_version(
                    contact_id=contact.id,
                    user_id=user.id,
                    admin_id=second_user.id,
                    base_date=base_date + timedelta(days=i * random.randint(10, 20))
                )
                versions.append(version)
            
            db.add_all(versions)
        
        db.commit()

    # Add some sample version history for the first contact
    old_versions = [
        models.ContactVersion(
            contact_id=contacts[0].id,
            first_name="Johnny",
            last_name="Doe",
            email="johnny.doe@example.com",
            phone="+1 234 567 8900",
            modified_by_id=second_user.id,  # Modified by admin
            created_at=datetime.now(timezone.utc) - timedelta(days=30)
        ),
        models.ContactVersion(
            contact_id=contacts[0].id,
            first_name="John",
            last_name="Doe Jr",
            email="john.jr@example.com",
            phone="+1 234 567 8900",
            modified_by_id=user.id,  # Modified by regular user
            created_at=datetime.now(timezone.utc) - timedelta(days=15)
        )
    ]
    db.add_all(old_versions)
    db.commit() 