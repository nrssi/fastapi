from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import json

server = FastAPI()
# Implementing simple CRUD operations for the Pet 
# Pet will contain all the data required for the storage

# BaseModel class from pydantic provides type validation, dictionary conversion
# json conversion and many more helper functions for data transport and storage 
class Pet(BaseModel):
    name:str
    age:int
    type:Union[str,None] = None


# A temporary list to contain all the available pets 
# the data stored in this list is written to database.json file in current directory
# and the data is written to this file with each modification operation like 
# create, update and delete.
# the same file is read during the startup routine of the server.
pets_list = []

# function takes all the values present in "pets_list" list and then writes it to 
# database.json file. 
def write_pets():
    outputfile =  open("database.json", "w")
    pets = {}
    for i in range(0, len(pets_list)):
        pets[i] = dict(pets_list[i])
    json.dump(pets, outputfile)
    close(outputfile)


# function reads the database.json file in current directory and then converts the 
# available data to a python dictionary.
def read_pets():
    try:
        outputfile = open("database.json", "x")
        close(outputfile)
    except FileExistsError:
        outputfile = open("database.json", "r")
        try:
            pet_dict = json.load(outputfile)
            for i in range(0, len(pet_dict)):
                pets_list.append(Pet(name=pet_dict[str(i)]["name"], age=pet_dict[str(i)]["age"], type=pet_dict[str(i)]["type"]))
        except json.decoder.JSONDecodeError:
            print("Error parsing the json file.")
        return

# the startup function executes on after starting the server
@server.on_event("startup")
def startup():
    read_pets()


@server.on_event("shutdown")
def shutdown_func():
    write_pets()


# index page for our website Lol :>
@server.get("/")
async def hello():
	return {"text" : "hello"}

# 22-08-2022's assignment, implementing basic arithmetic operations and returning 
# the results to the user in json format
@server.get("/arm_operations")
async def arithmetic_operations(first_number:int, second_number:int):
    if second_number == 0:
        return {"error" : "Division By Zero"}
    else:
        sum = first_number + second_number
        prod = first_number * second_number
        diff = first_number - second_number
        quo = first_number / second_number
        return {"Sum" : sum, "Difference" : diff, "Product" : prod, "Quotient" : quo}


# the function executed on a post request to "/create" path
# Parameters => all parameters passed are query parameters 
#   name : refers to the name of the pet (required as there's no default value)
#   age : refers to the age of the pet (required as there's no default value)
#   type : refers to the breed of species of the pet (optional, "Unkown" acts as the default value)
#
# Return value => 
#    A message saying the pet is added to the list 
@server.post("/create")
async def create_pet(pet:Pet):
        pets_list.append(pet)
        return {"msg" : f"{pet.name} is added to the list"}


# executes on a get request to "/read" path 
# Parameters => no parameters required 
# 
# Return value => 
#   returns all the available pets in json format
#   return a message if the "pets_list" list is empty 
@server.get("/read")
async def read_pets():
    if len(pets_list) == 0:
        return {"msg" : "No pets added yet"}
    else:
        pets = {}
        for i in range(0, len(pets_list)):
            pets[i] = dict(pets_list[i])
        return pets

# executes on a get request to "/update" path 
# Parameters => mixed parameters 
#   index : refers to index of pet in "pets_list" list (path parameter)
#   Query Parameters =>
#       name : refers to the name of the pet (optional, "" acts as default value)
#       age : refers to the age of the pet (optional, -1 acts as the default value)
#       type : refers to the type of the pet (optional, "Unknown" acts as the default value)
#
# Return value => 
#   returns a message saying invalid index if the index is out of bounds
#   returns a message saying pets details are updated
@server.get("/update/{index}")
async def update_pet(index:int, name:str="", age:int=-1, type:str="Unknown"):
    try:
        if name == "":
            name = pets_list[index].name
        if age == -1:
            age = pets_list[index].age
        if type == "Unknown":
            type = pets_list[index].type
        pets_list[index] = Pet(name=name, age=age, type=type)
    except IndexError:
        return {"msg" : "Invalid index"}
    else:
        return {"msg" : f"{name} is updated in the list"}

# executes on a get request to "/delete" path 
# Parameters => all parameters are query parameters 
#   index : refers to the index of pet in the "pets_list" list.
#
# Return value => 
#   returns a message saying invalid index if the index is out of bounds 
#   returns a message saying pet is deleted
@server.get("/delete")
async def delete_pet(index:int=0):
    if index>len(pets_list)-1:
        return {"msg" : "Invalid index"}
    else:
        del pets_list[index]
        return {"msg" : f"Pet {index} deleted from the list"}


@server.get("/get")
async def get_pet_details(index:int):
    if index>len(pets_list)-1:
        return {"msg" : "Invalid index"}
    else:
        return pets_list[index].dict()
