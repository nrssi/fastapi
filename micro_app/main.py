from fastapi import FastAPI, HTTPException
from .routers import connection, retrieve, create
app = FastAPI()
app.include_router(connection.router)
app.include_router(create.router)
app.include_router(retrieve.router)

@app.get("/")
@connection.connection_required
def index():
    return {"detail": "Hello World"}
