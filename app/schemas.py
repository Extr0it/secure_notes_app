#schemas.py definește CE date primește și CE date trimite API-ul, pentru fiecare caz.

from pydantic import BaseModel, Field #verifica datele si transforma JSON <-> obct python

class UserCreate(BaseModel): #asteptam de la user
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)

class UserOut(BaseModel): #le da mai departe la frontend/API (nu pt user)
    id:int
    username: str
    class Config: 
        from_attributes = True
        #Spune CUM să construiască schema(pentru Pydantic)

class Token(BaseModel):
    access_token: str  #asta e biletul de acces pt frontend, e salvat si trimis mai departe la fiecare request
    token_type: str = "bearer"

class NoteCreate(BaseModel):
    title: str
    content: str
    class Config:
        from_attributes = True

class NoteOut(BaseModel):
    id:int
    title: str
    content: str

    class Config:
        from_attributes = True