import colorama
from typing import List
import subprocess, os, sys, inspect
from ..helpers import create_parquet
from sqlalchemy.orm import decl_api, sessionmaker, declarative_base
from fastapi import APIRouter, HTTPException
from pyspark.sql import SparkSession

from .connection import connection_required, create_engine, conn_str, engine
from .. import models
colorama.init(autoreset=True)
os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
os.environ["PATH"] += f';{os.environ["HADOOP_HOME"]}\\bin'


spark = SparkSession.builder.appName("Local Creator").getOrCreate()
router = APIRouter(prefix="/archive")

@router.post("/")
@connection_required
async def archive_all():
    pass

@router.post("/schema")
@connection_required
async def archive_schema(schema:str, archive_details:models.ArchiveInfo):
    global engine
    create_parquet(engine, [schema])
    return {"msg" : "Creation of parquet files for all tables completed successfully"}

@router.post("/table")
@connection_required
async def archive_table(schema:str, table:List[str]):
    global engine 
    print("schema= ", schema, "table = ",table)
    create_parquet(engine, [schema], table)
    return {"msg" : "Creation of parquet files for all tables completed successfully"}