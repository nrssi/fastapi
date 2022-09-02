from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine, sql
from sqlalchemy.orm import sessionmaker, Session
from typing import Union
import crud


server = FastAPI()
db_connection = None
SessionLocal = None
engine = None

class DataBaseDetails(BaseModel):
    ip : str
    port : int
    username : str
    password : str
    database_name : str

def get_db():
    if not SessionLocal:
        print("create a connection first")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@server.on_event("startup")
async def connection():
    DB_URL = "mysql+pymysql://root:estuate@localhost:3300/pets"
    global engine
    engine = create_engine(DB_URL, echo=True)
    try:
        global db_connection
        db_connection = engine.connect()
        global SessionLocal
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        crud.Base.metadata.create_all(bind=engine)
        return {"msg" : f"Connection to MySQL server at localhost:3300 was successful"}
    except Exception as e:
        return {"msg" : f"there was some error connecting to the server : {e}"}

@server.get("/get/{id}", response_model=crud.PetsForm)
async def get_pets(id : int, db:Session = Depends(get_db)):
    result = crud.get_pet(db, id)
    return result
@server.put("/create")
async def create_pet(pet : crud.PetsForm, db : Session = Depends(get_db)):
    result = crud.insert_pet(db, pet)
    return result

@server.post("/update")
async def update_pet(pet_id: int, details : crud.PetsForm, db : Session = Depends(get_db)):
    result = crud.update_pet(db, pet_id, details)
    return result

@server.delete("/delete")
async def delete_pet(pet_id : int, db : Session = Depends(get_db)):
    result = crud.delete_pet(db, pet_id)
    return result

@server.get("/get_by_name")
async def get_pet_by_name(pet_name : str, db : Session = Depends(get_db)):
    result = crud.get_pet_by_name(db, pet_name)
    return result

@server.get("/get_all")
async def get_all_pets(db : Session = Depends(get_db)):
    result = crud.get_all_pets(db)
    return result