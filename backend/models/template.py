from pydantic import BaseModel

class Template(BaseModel):
    title: str
    image_url: str
    link: str
    source: str
