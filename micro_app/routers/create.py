from fastapi import APIRouter
from pyspark.sql import SparkSession
import os
from .connection import connection_required, connection_details
router = APIRouter(prefix="/create")


@router.post("/")
@connection_required
def create_parquet():
    os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
    os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
    os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
    os.environ["PATH"] += f';{os.environ["HADOOP_HOME"]}\\bin'
    spark = SparkSession.builder.appName("Local Creator").getOrCreate()
    return {"msg": "success"}
