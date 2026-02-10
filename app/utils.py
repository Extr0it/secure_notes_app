import os
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

def read_key(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#deprecated :dacă pe viitor schimbi algoritmul, știe să verifice și parole vechi

#luate din schemas
JWT_PRIVATE_KEY_FILE = os.getenv("JWT_PRIVATE_KEY_FILE")
JWT_PUBLIC_KEY_FILE  = os.getenv("JWT_PUBLIC_KEY_FILE")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Pentru HS256 ai nevoie de un secret, nu de chei RSA
JWT_SECRET = os.getenv("JWT_SECRET")

# Citim cheile doar dacă folosim algoritmi RSA/EC și avem fișierele setate
PRIVATE_KEY = None
PUBLIC_KEY = None

if ALGORITHM.upper().startswith(("RS", "ES")):
    if not JWT_PRIVATE_KEY_FILE or not JWT_PUBLIC_KEY_FILE:
        raise RuntimeError(
            "JWT_PRIVATE_KEY_FILE / JWT_PUBLIC_KEY_FILE lipsesc din env, dar folosesti RS*/ES*."
        )

    PRIVATE_KEY = read_key(JWT_PRIVATE_KEY_FILE).strip()
    PUBLIC_KEY  = read_key(JWT_PUBLIC_KEY_FILE).strip()
else:
    # HS256/HS512 etc.
    if not JWT_SECRET:
        raise RuntimeError(
            "JWT_SECRET lipseste din env, dar folosesti HS* (ex: HS256)."
        )

#metoda care face criptarea parolelor
def hash_password(password:str) -> str:
    return pwd_context.hash(password) #.hash e generica cryptcontext


#metoda care verifica parolele daca matchuiesc cu DB
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
#.verify e generica de asemenea



#metoda care creeaza biletul de acces(TOKENU) pt a vb cu serverul
def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    #payload-ul e ca sa stie pentru cine e acest token
    payload = {"sub": subject, "exp": expire}

    #aici e magia adevarata, comina toate 3 si creeaza un string lung, acela e TOKENUL adevarat (mereu e diferit)
    if ALGORITHM.upper().startswith(("RS", "ES")):
        return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
    else:
        return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)



#metoda care decodeaza tokenul, deoarece SERVERUL are mai multi useri si nu stie cine ce token are din minte, asa ca trebuie trimis cu fiecare request al userului (si serveru DECODEAZA)
def decode_access_token(token: str):
    try:
        if ALGORITHM.upper().startswith(("RS", "ES")):
            return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        else:
            return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        return None