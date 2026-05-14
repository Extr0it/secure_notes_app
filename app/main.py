from fastapi import FastAPI, Depends
#Dependency injection
from app.database import engine,SessionLocal
from app.models import Note, User
from sqlalchemy.orm import Session
from app.database import Base
from app.security import encrypt, decrypt, hash_password, verify_password, create_access_token, get_current_user
from app.schemas import NoteCreate, NoteDelete, NoteModify, UserCreate
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware #CORS

app = FastAPI()
# notes = {} #am implementat un dict ca test
Base.metadata.create_all(bind=engine) #creeaza clasele in db


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
      db = SessionLocal()
      try:
            yield db #pauză + memorează unde ai rămas
      finally:
            db.close()


@app.get("/")   #fiecare reprezinta un endpoint
async def root(): 
        return {"message" : "Hello World"}


@app.get("/notes") 
async def get_note(
      current_user : User = Depends(get_current_user), #alt doilea dependency injection pt TOKEN
      db: Session = Depends(get_db)):
         
         results = db.query(Note).filter(Note.user == current_user.username).all() #returnează listă

         if not results:
           return {"msg": "userul nu exista sau nu are note"}
         
         return [ #returneaza dict pe care o vede doar clientu
        {
          "id": r.id,
          "title": r.title,
          "content": decrypt(r.encrypted_content)
        }
          for r in results
          ]
      

@app.post("/notes")
async def create_note(
      note_data: NoteCreate ,
      current_user : User = Depends(get_current_user), 
      db: Session = Depends(get_db)):
       
       #facem instanta de clasa Note
       new_note = Note( 
             user = current_user.username ,#user, atributul user din clasă primește parametrul user din funcție.
             title = note_data.title, #JSON
             encrypted_content = encrypt(note_data.content) #JSON
       )
       db.add(new_note)
       db.commit() #salveaza in db
       db.refresh(new_note) #ii aloca un id

       return { #returneaza dict pe care o vede doar clientu
             "id": new_note.id,
              "user": new_note.user,
              "title" : new_note.title,
              "content" : decrypt(new_note.encrypted_content)
        } #aici nu e nevoie de for pt ca avem obiect nu lista
       


@app.delete("/notes/all") #sterge toate notele
async def delete_all_notes(
      current_user : User = Depends(get_current_user), 
      db: Session = Depends(get_db)):

      notes = db.query(Note).filter(Note.user == current_user.username).all() #returnează listă
      
      if not notes:
            return {"msg" : "userul nu exista"}

      for note in notes:
            db.delete(note)

      db.commit()
      return {"msg" : "operatie cu succes"}


@app.delete("/notes") #sterge doar 1 nota
async def delete_note(
      note_data: NoteDelete, 
      current_user : User = Depends(get_current_user),
      db: Session = Depends(get_db)):
        
        db_note = db.query(Note).filter(Note.user ==current_user.username, Note.title ==note_data.title).first()
         
        if not db_note:
            return {"msg" : "notita nu exista❌"}
      
        db.delete(db_note)
        db.commit()
      
        return {"msg" : "operatie cu succes✅"}
         
@app.put("/notes")
async def modify_note(
    note_data: NoteModify,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(
        Note.user == current_user.username,
        Note.title == note_data.title
    ).first()

    if not db_note:
        return {"msg": "notita nu exista❌"}
    
    db_note.encrypted_content = encrypt(note_data.content)

    db.commit()
    db.refresh(db_note)

    return { "id" : db_note.id, 
             "user" : db_note.user,
             "title": db_note.title,
             "content": decrypt(db_note.encrypted_content)
            }

@app.post("/register")
async def register_user(
      user_data : UserCreate, 
      db: Session = Depends(get_db)):

      db_user = db.query(User).filter(
            User.username == user_data.username,   
      ).first()

      if db_user :
            return {"msg" :"!user deja existent!"}
      
      new_user = User(
            username = user_data.username,
            hashed_pw = hash_password(user_data.password)

      )

      db.add(new_user)
      db.commit()
      db.refresh(new_user)

      return {"msg" : f"Username {user_data.username} a fost adaugat"}


@app.post("/login")
async def login_user(
      form_data: OAuth2PasswordRequestForm = Depends(),
      db: Session = Depends(get_db) ):

      db_user = db.query(User).filter(
            User.username == form_data.username,  
      ).first()
      
      if not db_user :
            return {"msg" :"Username introdus incorect!"}
      
      if not verify_password(form_data.password, db_user.hashed_pw):
            return {"msg" : "Parola introdusa incorect!"}

      #------TOKEN------------
      access_token = create_access_token( 
      data={"sub": db_user.username}
       )

      return {
       "access_token": access_token,
       "token_type": "bearer"
       }#----------


























#pentru varianta cu dictionar------------------

# @app.post("/notes/{user}/{title}")
# async def create_note(user: str, title: str):
#         if user not in notes:
#                 notes[user] = []
        
#         notes[user].append(title)
#         return notes[user]

# @app.delete("/notes/{user}")
# async def delete_user(user: str):
#         if user not in notes:
#             return {"msg" : "userul nu mai exista"}
        
#         notes.pop(user)
#         return {"operatiune de succes"}


# @app.delete("/notes/{user}/{title}")
# async def delete_note(user: str, title:str):
#         if user not in notes or title not in notes[user]:
#             return {"msg" : "userul/notita nu exista"}
#         notes[user].remove(title)

# @app.put("/notes/{user}/{title}/{nou}")
# async def modify_note(user: str, title:str, nou:str):
#         if user not in notes or title not in notes[user]:
#             return {"msg" : "userul/notita nu exista"}
        
#         index = notes[user].index(title)
#         notes[user][index] = nou
#         return {"notes" : notes[user]}
        

       
       
