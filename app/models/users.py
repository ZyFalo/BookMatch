"""
Esquema para la colección "quotes" de la base de datos BookMatch.

Este módulo define la estructura y validación para las citas.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    """Clase auxiliar para convertir entre ObjectId y string."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class QuoteModel(BaseModel):
    """
    Modelo Pydantic para la colección 'quotes'.
    
    Estructura:
    - id: ID único de MongoDB
    - quote: Texto de la cita
    - author: Autor de la cita
    - image_url: URL de la imagen asociada a la cita
    - tags: Lista de etiquetas relacionadas
    - source: Fuente de la cita (por ejemplo, 'goodreads')
    - created_at: Fecha de creación del registro
    """
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    quote: str
    author: str
    image_url: Optional[str] = None
    tags: List[str] = []
    source: str = "goodreads"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Configuración del modelo."""
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
        schema_extra = {
            "example": {
                "quote": "No te preocupes si funciona bien. Si todo estuviera correcto, sería despedido de mi trabajo.",
                "author": "Mosher's Law of Software Engineering",
                "image_url": "https://images.gr-assets.com/quotes/1234567890p2/12345.jpg",
                "tags": ["humor", "programming", "software"],
                "source": "goodreads"
            }
        }

class QuoteResponse(BaseModel):
    """Modelo para la respuesta al crear o actualizar una cita."""
    quote: str
    author: str
    id: str = Field(..., alias="_id")

    class Config:
        """Configuración del modelo de respuesta."""
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# Esquema de validación para MongoDB
quote_validation_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["quote", "author", "source"],
        "properties": {
            "quote": {
                "bsonType": "string",
                "description": "Texto de la cita"
            },
            "author": {
                "bsonType": "string",
                "description": "Autor de la cita"
            },
            "image_url": {
                "bsonType": ["string", "null"],
                "description": "URL de la imagen asociada a la cita"
            },
            "tags": {
                "bsonType": "array",
                "description": "Lista de etiquetas relacionadas",
                "items": {
                    "bsonType": "string"
                }
            },
            "source": {
                "bsonType": "string",
                "description": "Fuente de la cita"
            },
            "created_at": {
                "bsonType": "date",
                "description": "Fecha de creación del registro"
            }
        }
    }
}