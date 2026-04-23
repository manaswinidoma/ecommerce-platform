# It represents how data looks at the API Boundary. What comes in from the request, what goes out in the response.

from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    firstname: str = Field(min_length=1, max_length=100)
    lastname: str = Field(min_length=1, max_length=100)
    email: EmailStr 
    password: str = Field(min_length=8)
    date_of_birth: Optional[date] = None 
    
class UserLogin(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8)     # UserRegister and UserLogin receive plain JSON from the client, not database objects.
    
class UserResponse(BaseModel):
    user_id: int
    username: str = Field(min_length=1, max_length=100)
    firstname: str = Field(min_length=1, max_length=100)
    lastname: str = Field(min_length=1, max_length=100)
    email: EmailStr 
    date_of_birth: Optional[date] = None 
    user_role: str = Field(default='customer')
    created_at: datetime 
    last_login: Optional[datetime] = None
    class Config:               # pydantic--> dict  sqlalchemy-->objs without if we return a SQLAlchemy User object as a UserResponse, Pydantic will throw an error.      
        from_attributes = True  # tells Pydantic "also accept objects with attributes, not just dictionaries."


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"