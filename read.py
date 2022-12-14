from pyspark.sql import SparkSession
import os , sys
def read_file(path:str):
    os.environ["SPARK_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2'
    os.environ["HADOOP_HOME"] = 'C:\\Users\\Shyam\\Documents\\spark-3.2.2-bin-hadoop3.2\\bin\\hadoop'
    os.environ["PYSPARK_PYTHON"] = 'C:\\Users\\Shyam\\Documents\\fastapi\\env\\Scripts\\python'
    os.environ["PATH"] += f';{os.environ["HADOOP_HOME"]}\\bin'
    spark = SparkSession.builder.appName("Parquet Reader").getOrCreate()
    try:
        df = spark.read.parquet(sys.argv[1])
        df.show()
        print("--------------------------------------------------")
        print("                     SCHEMA")
        print("--------------------------------------------------")
        df.printSchema()
        print("--------------------------------------------------\n\n")
        print("The total number of rows read form the archive : ", df.count())
        print("The total number of columns read from the archive : ", len(df.columns))
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    read_file(sys.argv[1])