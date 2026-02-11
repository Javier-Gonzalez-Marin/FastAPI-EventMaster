from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, get_db

# Crea las tablas en la base de datofrom fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, get_db

# Crea las tablas en la base de datos automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventMaster API")

# --- RECINTOS (CRUD) ---
@app.post("/recintos/", response_model=schemas.Recinto)
def crear_recinto(recinto: schemas.RecintoCreate, db: Session = Depends(get_db)):
    db_recinto = models.Recinto(**recinto.model_dump())
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto

@app.get("/recintos/", response_model=List[schemas.Recinto])
def listar_recintos(db: Session = Depends(get_db)):
    return db.query(models.Recinto).all()

# --- EVENTOS ---
@app.post("/eventos/", response_model=schemas.Evento)
def crear_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    db_evento = models.Evento(**evento.model_dump())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.get("/eventos/", response_model=List[schemas.Evento])
def leer_eventos(ciudad: str = Query(None), db: Session = Depends(get_db)):
    # Se utiliza .join() para vincular Evento con Recinto [cite: 47, 53]
    query = db.query(models.Evento).join(models.Recinto)
    if ciudad:
        # Se usa .ilike() para búsqueda insensible a mayúsculas [cite: 49, 54]
        query = query.filter(models.Recinto.ciudad.ilike(f"%{ciudad}%"))
    return query.all()

@app.patch("/eventos/{id}/comprar")
def comprar_tickets(id: int, cantidad: int, db: Session = Depends(get_db)):
    # 1. Buscar el evento [cite: 65]
    evento = db.query(models.Evento).filter(models.Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # 2, 3 y 4. Validar aforo comparando con la capacidad del recinto [cite: 66, 67, 68]
    if (evento.tickets_vendidos + cantidad) > evento.recinto.capacidad:
        # 5. Error 400 si se supera el aforo [cite: 34, 69, 71]
        raise HTTPException(status_code=400, detail="Aforo insuficiente en el recinto")

    evento.tickets_vendidos += cantidad
    db.commit()
    db.refresh(evento)
    return {"mensaje": "Compra exitosa", "tickets_vendidos": evento.tickets_vendidos}