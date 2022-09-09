from fastapi import FastAPI
from .routers import archive, connection, retrieve
app = FastAPI()
app.include_router(connection.router)
app.include_router(archive.router)
app.include_router(retrieve.router)


@app.get("/")
def index():
    return {"detail": "Hello World"}
