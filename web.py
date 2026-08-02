import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Global News Network",
    version="1.0.0",
)


WEBAPP_DIR = "webapp"


os.makedirs(
    WEBAPP_DIR,
    exist_ok=True,
)


STATIC_DIR = os.path.join(
    WEBAPP_DIR,
    "static",
)

os.makedirs(
    STATIC_DIR,
    exist_ok=True,
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
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
