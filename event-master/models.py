from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Recinto(Base):
    __tablename__ = "recintos"

    # Campos obligatorios del Recinto [cite: 15, 17, 18, 20]
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)

    # Relación: Un recinto tiene muchos eventos [cite: 60]
    eventos = relationship("Evento", back_populates="recinto")

class Evento(Base):
    __tablename__ = "eventos"

    # Campos obligatorios del Evento [cite: 22, 23, 24, 25, 26, 27]
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)
    precio = Column(Float, nullable=False)
    tickets_vendidos = Column(Integer, default=0)
    
    # Clave foránea hacia Recinto
    recinto_id = Column(Integer, ForeignKey("recintos.id"))

    # Relación: Un evento pertenece a un recinto [cite: 58, 59]
    recinto = relationship("Recinto", back_populates="eventos")