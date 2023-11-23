from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, date
from pydantic import BaseModel
from typing import List

from main import calculate_age

DATABASE_URL = "sqlite:///./morg_database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Corpse(Base):
    __tablename__ = "corpses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cause_of_death = Column(String)
    date_of_death = Column(Date)
    birth_date = Column(Date)
    age = Column(Integer)


Base.metadata.create_all(bind=engine)


class CorpseCreate(BaseModel):
    name: str
    cause_of_death: str
    date_of_death: date
    birth_date: date


class CorpseResponse(CorpseCreate):
    id: int
    age: int

    class Config:
        orm_mode = True


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/corpses/", response_model=CorpseResponse)
def create_corpse(corpse: CorpseCreate, db: Session = Depends(get_db)):
    corpse_db = Corpse(**corpse.dict(), age=calculate_age(corpse.birth_date, corpse.date_of_death))
    db.add(corpse_db)
    db.commit()
    db.refresh(corpse_db)
    return corpse_db


@app.get("/corpses/", response_model=List[CorpseResponse])
def read_corpses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    corpses = db.query(Corpse).offset(skip).limit(limit).all()
    return corpses


@app.get("/corpses/{corpse_id}", response_model=CorpseResponse)
def read_corpse(corpse_id: int, db: Session = Depends(get_db)):
    corpse = db.query(Corpse).filter(Corpse.id == corpse_id).first()
    if corpse is None:
        raise HTTPException(status_code=404, detail="Corpse not found")
    return corpse


@app.put("/corpses/{corpse_id}", response_model=CorpseResponse)
def update_corpse(corpse_id: int, corpse: CorpseCreate, db: Session = Depends(get_db)):
    existing_corpse = db.query(Corpse).filter(Corpse.id == corpse_id).first()
    if existing_corpse is None:
        raise HTTPException(status_code=404, detail="Corpse not found")

    # Обновление полей
    existing_corpse.name = corpse.name
    existing_corpse.cause_of_death = corpse.cause_of_death
    existing_corpse.date_of_death = corpse.date_of_death
    existing_corpse.birth_date = corpse.birth_date
    existing_corpse.age = calculate_age(corpse.birth_date, corpse.date_of_death)

    db.commit()
    db.refresh(existing_corpse)
    return existing_corpse


@app.delete("/corpses/{corpse_id}", response_model=dict)
def delete_corpse(corpse_id: int, db: Session = Depends(get_db)):
    corpse = db.query(Corpse).filter(Corpse.id == corpse_id).first()
    if corpse is None:
        raise HTTPException(status_code=404, detail="Corpse not found")

    db.delete(corpse)
    db.commit()
    return {"message": "Corpse deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
