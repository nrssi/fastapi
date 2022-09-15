from fastapi import APIRouter, HTTPException
from copy import deepcopy
from ..config import config
from sqlalchemy import create_engine
from ..models import DBInfo

router = APIRouter(prefix="/connect")


@router.post("/")
async def connect(details: DBInfo):
    dialect = "pyodbc"
    if details.database_server == "mysql":
        dialect = "pymysql"
    elif details.database_server == "oracle":
        dialect = "cx_oracle"
    elif details.database_server == "mssql":
        dialect = "pymssql"
    config.conn_str = f"{details.database_server}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/"
    try:
        config.engine = create_engine(config.conn_str)
        config.connection_details = deepcopy(details)
        config.engine.connect()
        return {"detail" : "Connection Successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")