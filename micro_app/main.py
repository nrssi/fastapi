from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import archive, connection, retrieve
app = FastAPI()
app.include_router(connection.router)
app.include_router(archive.router)
app.include_router(retrieve.router)


@app.get("/", response_class=HTMLResponse)
def index():
    return "<h1>Hello, World</h1>"
