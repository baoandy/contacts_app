from fastapi import HTTPException

class ContactException(HTTPException):
    """Base exception for contact-related errors"""
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class DuplicateEmailError(ContactException):
    """Raised when attempting to create a contact with an email that already exists"""
    def __init__(self):
        super().__init__(detail="A contact with this email already exists. Please use a different email.") 

class InvalidPhoneNumberError(ContactException):
    """Raised when attempting to create a contact with an invalid phone number"""
    def __init__(self):
        super().__init__(detail="Invalid phone number. Please enter a valid phone number.")