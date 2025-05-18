from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler
from typing import Optional, Any, Annotated
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# Implementación actualizada para Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            json_schema=core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
    full_name: str
    email: EmailStr

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }

class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: str
    full_name: str
    current_password: Optional[str] = None
    new_password: Optional[str] = None
