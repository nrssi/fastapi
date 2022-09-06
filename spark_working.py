from functools import wraps
from json import load
import os
import inspect
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, decl_api
from pyspark.sql import SparkSession
import models

engine = create_engine(
    "mysql+pymysql://root:estuate@localhost:3300/classicmodels")
conn = engine.connect()
models.Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
os.environ["path"] += f';{os.environ["HADOOP_HOME"]}\\bin'

spark = SparkSession.builder.appName("Data Archiver").getOrCreate()

def get_dict(obj: models.Base):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields


tables = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules["models"]) if inspect.isclass(
    cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]

for table in tables:
    print("---------------------------------------------------------------------")
    print("                         ", table.__name__)
    print("---------------------------------------------------------------------")
    result = db.query(table).all()
    result = list(map(get_dict, result))
    df = spark.createDataFrame(result)
    df.repartition(1).write.option("compression", "snappy").parquet(f"dest/{table.__name__}")
