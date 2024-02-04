from pydantic import BaseModel


class Script(BaseModel):
    code: str
