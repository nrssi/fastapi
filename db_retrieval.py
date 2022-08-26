from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine, sql
from sqlalchemy.orm import sessionmaker, Session
from typing import Union
import crud
import json


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
def config_reload(details):
    try:
        outpufile = open("config.json", "x")
        print("[INFO]   Creating the config.json file due to first run")
    except:
        outputfile = open("config.json", "r")
@server.on_event("startup")
async def connection():
    DB_URL = "mysql+pymysql://root:estuate@localhost:3300/pets"
    global engine
    engine = create_engine(DB_URL)
    try:
        global db_connection
        db_connection = engine.connect()
        global SessionLocal
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        crud.Base.metadata.create_all(bind=engine)
        config_reload(details)
        return {"msg" : f"Connection to MySQL server at {details.ip}:{details.port} was successful"}
    except Exception as e:
        return {"msg" : f"there was some error connecting to the server : {e}"}

@server.get("/get/{id}", response_model=crud.PetsForm)
async def get_pets(id : int, db:Session = Depends(get_db)):
    result = crud.get_pet(db, id)
    return result
@server.get("/get_by_name/{name}")
async def get_pets_by_name(name : str, db : Session = Depends(get_db)):
    result = crud.get_pet_by_name(db, name)
    return result

@server.post("/create")
async def create_pet(pet : crud.PetsForm, db : Session = Depends(get_db)):
    result = crud.insert_pet(db, pet)
    return result

@server.post("/update")
async def update_pet(pet_name : str, details : crud.PetsForm, db : Session = Depends(get_db)):
    result = crud.update_pet(db, id, details)
    return result
