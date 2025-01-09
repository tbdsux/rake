import json

from fastapi import FastAPI, Response

from app.router import api_router
from app.settings import get_config

app = FastAPI()


app.include_router(api_router)


@app.get("/")
def root():
    return Response(
        content=json.dumps(
            {"message": "Rake!", "config": get_config().model_dump(mode="json")}
        ),
        media_type="application/json",
    )
