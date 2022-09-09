from fastapi import APIRouter
from sqlalchemy import inspect
from micro_app.models import DBInfo
from .connection import create_engine
from ..helpers import connection_required
from ..config import config
import json
router = APIRouter(prefix="/retrieve")


@router.get("/schemas")
@connection_required
async def get_schemas():
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+pymysql://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/")
    inspector = inspect(engine)
    result = inspector.get_schema_names()
    return result


@router.get("/tables")
@connection_required
async def get_tables(schema_name: str):
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+pymysql://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/{schema_name}")
    inspector = inspect(engine)
    result = inspector.get_table_names()
    return result


@router.get("/metadata")
@connection_required
async def get_metadata(schema_name: str, table_name: str):
    connection_details = config.connection_details
    engine = create_engine(
        f"{connection_details.database_name}+pymysql://{connection_details.username}:{connection_details.password}@{connection_details.ip_address}:{connection_details.port_number}/{schema_name}")
    inspector = inspect(engine)
    result = inspector.get_columns(table_name)
    return f"{result}"