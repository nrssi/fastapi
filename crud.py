from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import HTTPException
import copy
Base = declarative_base()

class Pets(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key = True)
    name = Column(String(30)) 
    age = Column(Integer)
    type = Column(String(30))
    
    def __repr__(self) -> str:
        return f"<Pet id = {self.id}, name = {self.name}, age = {self.age}, type = {self.type}>"


class PetsForm(BaseModel):
    name : str
    age : int
    type : str
    class Config:
        orm_mode = True


def get_pet(db:Session, id : int):
    result = db.query(Pets).filter(Pets.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"No Pet by id : {id} found")
    else:
        return result

def get_all(db : Session):
    result = db.query(Pets).all()
    return result
def get_pet_by_name(db:Session, name : str):
    result = db.query(Pets).filter(Pets.name == name).all()
    if not result:
        raise HTTPException(status_code=404, detail=f"No Pet by name {name} found")
    else:
        return result

def get_all_pets(db:Session):
    return  db.query(Pets).all()

def insert_pet(db : Session, details : PetsForm):
    pet = Pets(name=details.name, age = details.age, type=details.type)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet

def update_pet(db:Session, pet_id: int, details : PetsForm):
    print("the value of id is : ", pet_id)
    result = db.query(Pets).filter(Pets.id == pet_id).first()
    print(type(result), type(details))
    result.name = details.name
    result.age = details.age
    result.type = details.type
    db.commit()
    return result

def delete_pet(db : Session, pet_id : int):
    result = db.query(Pets).filter(Pets.id == pet_id).first()
    tmp = copy.deepcopy(result)
    db.delete(result)
    db.commit()
    return tmp 
