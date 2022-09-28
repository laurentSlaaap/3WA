from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field as PydanticField

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Melody(BaseModel):
    id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")
    melody_b64: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {ObjectId: str}

class MelodyUpdate(BaseModel):
    melody_b64: Optional[str]



