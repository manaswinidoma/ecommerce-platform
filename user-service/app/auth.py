# To handle passwords and tokens
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

load_dotenv()
secret = os.getenv("SECRET_KEY")
algorithm = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # "I am using bcrypt. If bcrypt is ever deemed insecure, automatically flag it so I can move to a newer scheme."

def hash_password(password):
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd

def verify_password(plain_password, hashed_password):
    is_correct = pwd_context.verify(plain_password,hashed_password)
    return is_correct
       

def create_access_token(data):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, secret, algorithm=algorithm)
      
    
def verify_access_token(token):
    try:
        decoded_jwt = jwt.decode(token, secret, algorithms=[algorithm])
        return decoded_jwt
    except JWTError:        # catches both tampering AND expiry
        return None
        