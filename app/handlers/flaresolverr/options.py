from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from app.extra.types import ProxyOptions


class FlareRequestOptions(BaseModel):
    url: str
    max_timeout: int = 60000
    session: Optional[str] = None
    proxy: Optional[ProxyOptions] = None
    postData: Optional[str] = None


class FlareRequestConfig(BaseModel):
    endpoint: str


class FlareResponseSolution(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    url: str
    status: int
    headers: Dict[str, str]
    response: str
    cookies: List[Dict[str, Any]]
    userAgent: str


class FlareResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    solution: FlareResponseSolution
    status: str
    message: str
    startTimestamp: int
    endTimestamp: int
    version: str
