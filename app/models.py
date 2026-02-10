from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base
#folosim o librarie (sqlalchemy) cu care vom construi structura database ului prin python, si aici trb sa importam toate caracteristicile din librarie DE CARE AVEM NEVOIE 


#creeam structura
class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index = True)
  username = Column(String(100), unique = True, nullable=False, index=True) 
  hashed_password = Column(String(255), nullable=False)

  notes =relationship("Note", back_populates="owner", 
  cascade="all, delete-orphan"
  )
  # leagă clasa User de clasa Note,back_populates - ține relația coerentă în ambele sensuri(sa nu emarga obiectele), cascade- cand stergi owneru se duce si notita


class Note(Base):
  __tablename__ = "notes"

  id= Column(Integer, primary_key=True, index=True)
  title = Column(String(200), nullable=False)
  content = Column(Text, nullable=False)

  owner_id=Column(Integer, ForeignKey("users.id"), nullable=False, index=True) 
  owner = relationship("User", back_populates="notes")
  #Doar îți dă acces ușor la obiectul User din Python, daca trb modificat mai tarziu

