from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db #OBLIGATORIU: înregistrează modelele în Base

from app import models  # doar ca să încarce modelele
from .schemas import UserCreate, UserOut, Token, NoteCreate, NoteOut
from .utils import hash_password, verify_password, create_access_token, decode_access_token

from cryptography.fernet import Fernet
import os

Base.metadata.create_all(bind=engine) #creează tabelele din DB pe baza modelelor SQLAlchemy
app = FastAPI() #creeaza aplicatia FastAPI

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
#definește cum primește serverul tokenul JWT de la client

@app.get("/health")
def health():
    return {"status": "ok"}


#Când serverul primește un request POST /users, execută funcția de mai jos
@app.post("/users", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username ==payload.username).first() #cauta user in DB, .first() e necesar ca să obții UN obiect, nu o listă.

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
   
    user = models.User(
        username = payload.username,
        hashed_password=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#creem aceasta fctie inafara oricarui endpoint ca sa fie apelat din alta fct
def authenticate_user(db:Session, username : str, password:str):
    user = db.query(models.User).filter(models.User.username ==username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        #Dacă funcția verify_password(...) întoarce False, atunci:
        return None 
    return user


#POST /login primește username și parolă, verifică în baza de date dacă sunt corecte și respinge cererea cu 401 dacă nu sunt.
@app.post("/login", response_model=Token)
def login(form_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = authenticate_user(db, form_data.username, form_data.password)
     if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")
     
     #creeaza un token pe care il trimite clientului (cod de acces)
     token = create_access_token(subject=user.username)
     return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    payload = decode_access_token(token) 
    if not payload: #daca tokenul nu corespunde
         raise HTTPException(status_code=401, detail="Invalid token")
    
    #daca numele nu corespunde
    username = payload.get("sub") 
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    #daca useru din DB nu corespunde (cine stie ce probleme in spate)
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


#cand serverul primeste un request de tip post, se creeaza un note


@app.post("/notes", response_model=NoteOut)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
     #si acest note e pentur 
     note = models.Note(title=payload.title, content=payload.content, owner_id=user.id)
     db.add(note)
     db.commit()
     db.refresh(note)
     return note








    