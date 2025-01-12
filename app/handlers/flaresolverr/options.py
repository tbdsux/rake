from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from app.extra.types import ProxyOptions


class FlareRequestOptions(BaseModel):
    url: str
    max_timeout: int = 60000
    session: Optional[str] = None
    proxy: Optional[ProxyOptions] = None
    postData: Optional[str] = None
    cookies: Optional[List[Dict[str, Any]]] = None


class FlareRequestConfig(BaseModel):
    endpoint: str


class FlareResponseSolution(
    BaseModel,
):
    model_config = ConfigDict(from_attributes=True, strict=False, extra="allow")

    url: str
    status: int
    headers: Optional[Dict[str, str]] = None
    response: str
    cookies: List[Dict[str, Any]]
    userAgent: str


class FlareResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=False, extra="allow")

    solution: Optional[FlareResponseSolution] = None
    status: str
    message: str
    startTimestamp: Union[float, int]
    endTimestamp: Union[float, int]
    version: Optional[str] = None
