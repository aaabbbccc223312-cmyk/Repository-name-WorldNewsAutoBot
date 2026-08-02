from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Global News Network",
    version="1.0.0",
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

WEB_DIR = os.path.join(
    BASE_DIR,
    "web",
)

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static",
)


@app.get("/")
async def home():

    return FileResponse(
        os.path.join(
            WEB_DIR,
            "index.html",
        )
    )


@app.get("/health")
async def health():

    return {

        "status": "online",

        "service": "Global News Network",

    }
