from bs4 import BeautifulSoup
from pydantic import BaseModel


class Response(BaseModel):
    """
    Base class for all responses.
    """

    status: int
    message: str | None = None
    data: BeautifulSoup | None = None

    class Config:
        arbitrary_types_allowed = True
