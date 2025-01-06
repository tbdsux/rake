from typing import Optional

from pydantic import BaseModel


class ProxyOptions(BaseModel):
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
