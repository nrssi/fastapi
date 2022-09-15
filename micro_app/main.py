from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import archive, connection, retrieve
app = FastAPI()
app.include_router(connection.router)
app.include_router(archive.router)
app.include_router(retrieve.router)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=JetBrains Mono' rel='stylesheet'>
            <style>
            h1{
                font-family: 'JetBrains Mono';
                font-size: 22px;
                text-align: center;
            }
            </style>
        </head>
        <body>
            <h1>Hello, World</h1>
        </body>
    </html>"""

