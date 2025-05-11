from pydantic import BaseModel

class Template(BaseModel):
    title: str
    description: str
    thumbnail: str
    link: str
