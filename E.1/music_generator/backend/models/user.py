from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str

