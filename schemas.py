from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Esquemas para RECINTO (Venue) ---
class RecintoBase(BaseModel):
    nombre: str
    ciudad: str
    capacidad: int = Field(..., gt=0) # Debe ser mayor a 0

class RecintoCreate(RecintoBase):
    pass

class Recinto(RecintoBase):
    id: int

    class Config:
        from_attributes = True

# --- Esquemas para EVENTO (Event) ---
class EventoBase(BaseModel):
    nombre: str
    fecha: datetime
    # Requisito: El precio no puede ser negativo
    precio: float = Field(..., ge=0) 
    recinto_id: int

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id: int
    tickets_vendidos: int

    class Config:
        from_attributes = True