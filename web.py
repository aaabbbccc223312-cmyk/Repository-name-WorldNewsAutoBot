import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Global News Network",
    version="1.0.0",
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

WEBAPP_DIR = os.path.join(
    BASE_DIR,
    "webapp",
)

ASSETS_DIR = os.path.join(
    BASE_DIR,
    "assets",
)

os.makedirs(
    WEBAPP_DIR,
    exist_ok=True,
)

os.makedirs(
    ASSETS_DIR,
    exist_ok=True,
)

app.mount(
    "/assets",
    StaticFiles(directory=ASSETS_DIR),
    name="assets",
)


@app.get("/")
async def home():

    return FileResponse(
        os.path.join(
            WEBAPP_DIR,
            "index.html",
        )
    )


@app.get("/health")
async def health():

    return {
        "status": "online",
        "service": "Global News Network",
    }
