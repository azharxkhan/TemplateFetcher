from pydantic import BaseModel, HttpUrl
from typing import Optional

class Template(BaseModel):
    id: int
    title: str
    description: str
    thumbnail: HttpUrl
    url: HttpUrl
