from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
class Info(BaseModel):
    path:str 
    dest:str = "dest"
spark = SparkSession.builder.appName("csv file").getOrCreate()
server = FastAPI()
@server.post("/write")
async def write_csv(info:Info):
    df = spark.read.csv(info.path)
    df.write.parquet(info.dest)
    return {"message" : "Creating parquet file finished successfully"}