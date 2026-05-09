from pydantic import BaseModel


class NoteCreate(BaseModel):
    title:str
    content:str


class NoteDelete(BaseModel):
    title:str


class NoteModify(BaseModel):
    title: str
    content: str

class UserCreate(BaseModel):
    username : str
    password: str