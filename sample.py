import enum
import json
d = {
	"name" : "shyam",
	"age" : "21",
	"type" : "human"
	}
pet_list = []

try:
    outputfile = open("database.json", "x")
    print("Creating database.json file")
    outputfile.close()
except FileExistsError:
    outputfile = open("database.json", "r")
    print("Reading the database.json file")
    try:
        pet_dict = json.load(outputfile)
        for i in range(0, len(pet_dict)):
            print(pet_dict[str(i)])
            pet_list.append(pet_dict[str(i)]["name"])
            
    except json.decoder.JSONDecodeError:
        print("Error Decoding the json file")
print(pet_list)
