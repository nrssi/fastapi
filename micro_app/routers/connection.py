from fastapi import APIRouter, HTTPException
from copy import deepcopy
from ..config import config
from functools import wraps
from sqlalchemy import create_engine, exc
from ..models import DBInfo

router = APIRouter(prefix="/connect")


@router.post("/")
async def connect(details: DBInfo):
    dialect = "pyodbc"
    if details.database_name == "mysql":
        dialect = "pymysql"
    elif details.database_name == "oracle":
        dialect = "cx_oracle"
    elif details.database_name == "mssql":
        dialect == "pymssql"
    config.conn_str = f"{details.database_name}+{dialect}://{details.username}:{details.password}@{details.ip_address}:{details.port_number}/"
    try:
        config.engine = create_engine(config.conn_str)
        config.connection_details = deepcopy(details)
        config.engine.connect()
    except exc.NoSuchModuleError:
        raise HTTPException(status_code=404, detail="Unknown Database Server")
    except exc.OperationalError:
        raise HTTPException(
            status_code=404, detail="Wrong or missing Credentials")
    except exc.InterfaceError:
        raise HTTPException(
            status_code=404, detail="Dialect not specified or Data source name cannot be found")
    if not config.engine.connect():
        pass
    else:
        return {"msg": "Connection successfull"}

