import json 

with open("sample.json", "r") as infile:
    result = json.load(infile)
    print(result["name"], " and ", result["salary"])
    del result["age"]
    new_dict = {
        "employee_info":{
            "name" : result["name"], 
            "salary" : result["salary"]
        }
    }