from micro_app.models import ArchiveInfo, DBInfo
from .routers.connection import create_engine
from functools import wraps
from sqlalchemy.orm import decl_api, sessionmaker
from sqlalchemy import exc
import os
import subprocess
import colorama
import importlib
import sys
import inspect
import asyncio
from pyspark.sql import SparkSession
from fastapi import HTTPException
from typing import List, Any, Callable
from .config import config

colorama.init(autoreset=True)
os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
os.environ["PATH"] += f';{os.environ["HADOOP_HOME"]}\\bin'


spark = SparkSession.builder.appName("Local Creator").getOrCreate()


def get_dict(obj: decl_api.DeclarativeMeta):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields

def get_engine(details:DBInfo):
    pass

def create_parquet(engine, schemas: List[str], table_names: List[str] = [], details: ArchiveInfo = ArchiveInfo()):
    for schema in schemas:
        url = config.conn_str+schema
        print(colorama.Fore.GREEN+"INFO:", "\t  Connection URL : ", url)
        print(colorama.Fore.GREEN+"INFO:", "\t  Archiving Schema : ", schema)
        engine = create_engine(url)
        try:
            engine.connect()
        except exc.OperationalError:
            return {"detail" : f"No such schema found : {schema}"}
        except Exception as e:
            return {"detail" : f"{e}"}
        SessionLocal = sessionmaker(bind=engine)
        sqla_path = os.getcwd()+"\\env\\Scripts\\sqlacodegen.exe"
        print(colorama.Fore.GREEN+"INFO:",
              f"\t  Running Command : {sqla_path} {url} --outfile {schema}.py")
        result = subprocess.Popen([sqla_path, url, "--outfile", f"{schema}.py"]).wait()
        if result:
            return {"detail" : "Failed to generate ORM model"}
        try:
            table_module = importlib.__import__(schema)
            importlib.reload(table_module)
        except Exception as e:
            return {"detail" : "Import Error ORM model not compatible with SQLAlchemy"}
        if not table_names:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(
                cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]
            os.remove(f"{schema}.py")
            for table in tables:
                db = SessionLocal()
                result = db.query(table).all()
                result = list(map(get_dict, result))
                if not result:
                    continue
                try:
                    df = spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",
                          f"\t  Writing {table.__name__} to path : {details.path} using {details.compression_type} compression algorithm")
                    df.repartition(1).write.mode("overwrite").format("parquet").option(
                        "compression", details.compression_type).save(f"{details.path}/{schema}/{table.__name__}")
                except ValueError as ve:
                    return {"detail" : f"{ve}"}
        else:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(cls_obj) and isinstance(
                cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base" and cls_obj.__tablename__ in table_names]
            os.remove(f"{schema}.py")
            for table in tables:
                db = SessionLocal()
                result = db.query(table).all()
                result = list(map(get_dict, result))
                if not result:
                    continue
                try:
                    df = spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",
                          f"\t  Writing {table.__name__} to path : {details.path} using {details.compression_type} compression algorithm")
                    df.repartition(1).write.mode("overwrite").format("parquet").option(
                        "compression", details.compression_type).save(f"{details.path}/{schema}/{table.__name__}")
                except ValueError as e:
                    return {"detail" : f"{e}"}
        del table_module
    print(colorama.Fore.GREEN+"INFO:", "\t  create_paruet function call completed")
    return {"detail" : "Creation of parquet files executed successfully"}


# A decorator to check if a connection exists before calling the passed function
def connection_required(func: Callable) -> Callable:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            if not config.engine:
                raise HTTPException(
                    status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return await func(*args, **kwargs)
        return wrapper
    else:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if not config.engine:
                raise HTTPException(
                    status_code=403, detail="No live connection exists on the server, try to connect before doing this operation")
            else:
                return func(*args, **kwargs)
        return wrapper
