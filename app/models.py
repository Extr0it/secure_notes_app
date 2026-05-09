from sqlalchemy import Column,Integer, String
from database import Base #base e legatura dintre db si python

class Note(Base): #class Note extends Base(JAVA)
    __tablename__ = "notes"

    id = Column(Integer, primary_key= True)
    title = Column(String)
    user = Column(String)
    encrypted_content = Column(String)

class User(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String, unique=True)
    hashed_pw = Column(String)