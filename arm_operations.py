from fastapi import FastAPI
server = FastAPI()
# 22-08-2022's assignment, implementing basic arithmetic operations and 
# returning 
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
        return {"Sum" : sum,
                "Difference" : diff,
                "Product" : prod,
                "Quotient" : quo
            }

