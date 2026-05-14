from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta,timezone


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.database import SessionLocal
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv() #citeste env
key = os.getenv("FERNET_KEY")
cipher = Fernet(key)


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext( #instanta la clasa
    schemes=["bcrypt"], #algoritmul folosit pt hashing
    deprecated="auto" #compatibilitate cu hash uri vechi
)

def encrypt(text: str) -> str:
    encrypted = cipher.encrypt(text.encode())
    return encrypted.decode()

def decrypt(text: str) -> str:
    decrypted = cipher.decrypt(text.encode())
    return decrypted.decode()

# encode = string → bytes
# decode = bytes → string

def hash_password(password:str) :
    return pwd_context.hash(password) # chemi metodă pe obiect
   
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




#-------------------PARTEA DE TOKEN ------------------------

def create_access_token(data: dict): #functia de creeare token
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid"
            )

        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User invalid"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid sau expirat"
        )

    finally:
        db.close()