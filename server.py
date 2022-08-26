from fastapi import FastAPI
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine, sql
from pydantic import BaseModel
from typing import Union
import json


server = FastAPI()
# Implementing simple CRUD operations for the Pet 
# Pet will contain all the data required for the storage

# BaseModel class from pydantic provides type validation, dictionary conversion
# json conversion and many more helper functions for data transport and storage
class PetDetails(BaseModel):
    name:str
    age:int
    pet_type:Union[str,None] = None



# the startup function executes on after starting the server
@server.on_event("startup")
def startup():
    DB_URL = "mysql+pymysql://estuate:estuate@localhost:3300/pets"
    global engine
    engine = create_engine(DB_URL)
    metadata = MetaData()
    global pets_table 
    pets_table = Table(
            "pets", 
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(30)),
            Column('age', Integer),
            Column('type', String(30))
            )
    metadata.create_all(engine)
    global connection 
    connection = engine.connect()



@server.on_event("shutdown")
def shutdown_func():
    connection.disconnect()
    write_pets()


# index page for our website Lol :>
@server.get("/")
async def hello():
	return "extravagant" 


# the function executed on a post request to "/create" path
# Parameters => all parameters passed are query parameters 
#   name : refers to the name of the pet (required as there's no default value)
#   age : refers to the age of the pet (required as there's no default value)
#   type : refers to the breed of species of the pet 
#   (optional, "Unkown" acts as the default value)
#
# Return value => 
#    A message saying the pet is added to the list 
@server.post("/create")
async def create_pet(pet:PetDetails):
    stmt = pets_table.insert().values(name=pet.name, age=pet.age, type=pet.pet_type)
    result = connection.execute(stmt)
    return result

# executes on a get request to "/read" path 
# Parameters => no parameters required 
# 
# Return value => 
#   returns all the available pets in json format
#   return a message if the "pets_list" list is empty 
@server.get("/read")
async def read_pets():
    result = connection.execute(sql.select(pets_table))
    pets = {}
    for row in result:
        pets[row.id] = {"name" : row.name, "age" : row.age, "type" : row.type}
    return pets
# executes on a get request to "/update" path 
# Parameters => mixed parameters 
#   index : refers to index of pet in "pets_list" list (path parameter)
#   Query Parameters =>
#    name : refers to the name of the pet (optional, "" acts as default value)
#    age : refers to the age of the pet (optional,-1 acts as the default value)
#    type : refers to the type of the pet 
#    (optional, "Unknown" acts as the default value)
#
# Return value => 
#   returns a message saying invalid index if the index is out of bounds
#   returns a message saying pets details are updated
@server.get("/update")
async def update_pet(name:str, age:int, type:str):
    stmt = pets_table.update().where(pets_table.c.name == name).values(age=age, type = type)
    result = connection.execute(stmt)
    return result
# executes on a get request to "/delete" path 
# Parameters => all parameters are query parameters 
#   index : refers to the index of pet in the "pets_list" list.
#
# Return value => 
#   returns a message saying invalid index if the index is out of bounds 
#   returns a message saying pet is deleted
@server.get("/delete")
async def delete_pet(name:str):
    stmt = pets_table.delete().where(pets_table.c.name == name)
    print(pets_table.name, " and ", name)
    print(stmt)
    result = connection.execute(stmt)
    return result


@server.get("/get")
async def get_pet_details(name:str):
    stmt = pets_table.select().where(pets_table.c.name == name)
    result  = connection.execute(stmt)
    return  result.fetchone()
