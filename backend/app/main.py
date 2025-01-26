from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.db.database import engine, Base, get_db
from contextlib import asynccontextmanager
from app.db.seed import seed_data
from fastapi.middleware.cors import CORSMiddleware
from app.routes import contacts, users, websocket
from app.db.models import ContactVersion, Contact, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    seed_data(db)
    yield

    # Delete all data
    db.query(ContactVersion).delete()
    db.query(Contact).delete()
    db.query(User).delete()
    db.commit()

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(contacts.router)
app.include_router(websocket.router)