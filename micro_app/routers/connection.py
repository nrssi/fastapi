from functools import wraps
import asyncio
from typing import Callable, Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from ..models import DBInfo

engine = None
connection_details = DBInfo(database_name="mysql", username="root", schema_name="classicmodels", password="estuate", port_number=3300, ip_address="localhost")
conn_str = f"{connection_details.database_name}+pymysql://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/"

router = APIRouter(prefix="/connect")

engine = create_engine("mysql+pymysql://root:estuate@localhost:3300/classicmodels")
# @router.post("/")
# async def connect(details: DBInfo):
#     dialect = "pyodbc"
#     if details.database_name == "mysql":
#         dialect = "pymysql"
#     elif details.database_name == "oracle":
#         dialect = "cx_oracle"
#     elif details.database_name == "mssql":
#         dialect == "pymssql"
#     conn_string = f"{details.database_name}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/{details.schema_name}"
#     global engine
#     global connection_details
#     engine = create_engine(conn_string)
#     connection_details = details
#     if not engine.connect():
#         return {"msg": "Wrong or missing Credentials"}
#     else:
#         return {"msg": "Connection successfull"}


# A decorator to check if a connection exists before calling the passed function
def connection_required(func : Callable) -> Callable:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args:Any, **kwargs:Any):
            global engine
            if not engine:
                raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return await func(*args, **kwargs)
        return wrapper
    else:
        @wraps(func)
        def wrapper(*args:Any, **kwargs:Any):
            global engine
            if not engine:
                raise HTTPException(status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return func(*args, **kwargs)
        return wrapper