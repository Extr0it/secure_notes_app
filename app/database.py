import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
   "DATABASE_URL", "postgresql+psycopg2://postgres:password@db:5432/secure_notes")

engine = create_engine(  #trimite SQL către DB și primeste răspuns
    DATABASE_URL,
    pool_pre_ping= True, #verifică dacă legătura e vie înainte de use
    )

SessionLocal = sessionmaker(
   autocommit = False,             
   autoflush=False, 
   bind=engine) #o conversație controlată cu DB

Base = declarative_base() #TOT ce moștenește din mine = tabel, un fel de buton de implementare a claselor in db

def get_db():
    db=SessionLocal()
    try:  
      yield db  #o da endpointului 
      #Client → ENDPOINT → Server → Response
    finally:    
      db.close()  #fără finally → scurgeri de conexiuni





#docker exec -it secure_notes_db psql -U postgres -d secure_notes










