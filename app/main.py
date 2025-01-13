import json

from fastapi import FastAPI, Header, Response

from app.router import api_router
from app.settings import get_config

app = FastAPI()


app.include_router(api_router)


@app.get("/")
def root(
    real_ip: str = Header(None, alias="X-Real-IP"),
    forwarded_for: str = Header(None, alias="X-Forwarded-For"),
):
    return Response(
        content=json.dumps(
            {
                "message": "Rake!",
                "config": get_config().model_dump(mode="json"),
            }
        ),
        media_type="application/json",
    )
