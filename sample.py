from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine=None
DB_URL = "mysql+pymysql://estuate:estuate@localhost:3300/pets"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()
pets_table = Table(
    "pets",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('pet_type', String(30))
)
metadata.create_all(engine)
print("The Column names for the created table are : ", pets_table.columns.keys())

