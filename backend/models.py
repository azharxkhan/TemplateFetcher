from pydantic import BaseModel

class Template(BaseModel):
    id: int
    title: str
    description: str
    thumbnail: str