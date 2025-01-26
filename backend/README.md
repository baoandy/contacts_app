# Contacts App Backend

A FastAPI-based backend service for managing contacts with real-time updates via WebSocket.

## Project Description

This backend service provides a RESTful API and WebSocket endpoints for managing contacts. It features:

- Contact management (CRUD operations)
- Contact version history tracking
- Real-time updates via WebSocket
- User management
- PostgreSQL database integration

## Project Structure

```
backend/
├── app/
│   ├── db/
│   │   ├── database.py    # Database configuration
│   │   ├── models.py      # SQLAlchemy models
│   │   └── seed.py        # Database seeding
│   ├── routes/
│   │   ├── contacts.py    # Contact endpoints
│   │   ├── users.py       # User endpoints
│   │   └── websocket.py   # WebSocket endpoints
│   ├── main.py            # FastAPI application
│   └── websocket_connection_manager.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Dependencies

- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Uvicorn - ASGI server
- WebSockets - Real-time communication
- Other utilities (pydantic, phonenumbers)

## Running the Project

1. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. The API will be available at:
   - REST API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - WebSocket: ws://localhost:8000/ws

## Database

The application uses PostgreSQL with the following default configuration:
- Database: contactsdb
- User: postgres
- Password: postgres
- Port: 5432

Data is persisted using Docker volumes.

## Development

To run the application in development mode:

1. Make sure you have docker installed
2. Run `docker-compose up --build` to start the application
3. The API will be available at:
   - REST API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - WebSocket: ws://localhost:8000/ws
4. To reset the database, run `docker-compose down -v` and then `docker-compose up --build` again.