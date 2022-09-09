import colorama
import os
from typing import List
from ..helpers import create_parquet
from fastapi import APIRouter, HTTPException
from pyspark.sql import SparkSession
from ..config import config
from sqlalchemy import inspect
from .. import models
from ..helpers import connection_required
colorama.init(autoreset=True)
os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
os.environ["PATH"] += f';{os.environ["HADOOP_HOME"]}\\bin'


spark = SparkSession.builder.appName("Local Creator").getOrCreate()
router = APIRouter(prefix="/archive")


@router.post("/")
@connection_required
async def archive_all(archive_details:models.ArchiveInfo):
    engine = config.engine
    inspector = inspect(engine)
    schema_names = inspector.get_schema_names()
    create_parquet(engine, schema_names, details=archive_details)
    return {"msg": "Creation of parquet files for all tables completed successfully"}


@router.post("/schema")
@connection_required
async def archive_schema(schema: str, archive_details: models.ArchiveInfo):
    engine = config.engine
    create_parquet(engine, [schema])
    return {"msg": "Creation of parquet files for all tables completed successfully"}


@router.post("/table")
@connection_required
async def archive_table(schema: List[str], table: List[str], archive_details: models.ArchiveInfo):
    engine = config.engine
    create_parquet(engine, schema, table, archive_details)
    return {"msg": "Creation of parquet files for all tables completed successfully"}
