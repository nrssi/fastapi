from fastapi import APIRouter, HTTPException
from sqlalchemy import inspect, exc
from ..helpers import connection_required
from ..config import config



router = APIRouter(prefix="/retrieve")


@router.get("/schemas")
@connection_required
async def get_schemas():
    inspector = inspect(config.engine)
    result = inspector.get_schema_names()
    return {"SCHEMAS" : result}

@router.get("/tables")
@connection_required
async def get_tables(schema_name: str):
    inspector = inspect(config.engine)
    try:
        result = inspector.get_table_names(schema_name)
        return {"SCHEMA" : schema_name, "TABLES" : result}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database {schema_name} not found")


@router.get("/metadata")
@connection_required
async def get_metadata(schema_name: str, table_name: str):
    inspector = inspect(config.engine)
    try:
        result = inspector.get_columns(table_name, schema_name)
        fields = {"SCHEMA" : schema_name, "TABLE":table_name}
        for row in result:
            fields[f"{row['name']}"] = f"{row['type']}"
        return fields
    except exc.NoSuchTableError:
        raise HTTPException(status_code=500, detail=f"No table named {table_name} found")
    except exc.OperationalError:
        raise HTTPException(status_code=500, detail=f"No schema named {schema_name} found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

