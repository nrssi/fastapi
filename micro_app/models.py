from pydantic import BaseModel


class DBInfo(BaseModel):
    """Contains information related to connection of database"""
    database_server: str
    username: str
    password: str
    ip_address: str
    port_number: int


class ArchiveInfo(BaseModel):
    """Contains information related to archiving the files"""
    path: str = "dest"
    compression_type: str = "snappy"

