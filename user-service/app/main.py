from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session 
from datetime import datetime, timezone
from typing import List

from database import get_db, engine, Base
from schemas import UserLogin, UserRegister, UserResponse, TokenResponse, UserUpdate
import crud
import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)   # Creates all tables in the database automatically from models if they don't exist yet
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@app.get("/")
def root():
    return {"message": "E-Commerce User Service is running!"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload =  auth.verify_access_token(token)                      # Verifying the token then getting the payload
    if payload is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials!")

    user_id = int(payload.get("sub"))
    user = crud.get_user_by_id(db,user_id)                              # extract user id from payload and fetch user from db then return user
    
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials!")
    
    return user
     
        
@app.post("/users/register", response_model=UserResponse, status_code=201)
def register(new_user: UserRegister, db:Session = Depends(get_db)):
    if crud.get_user_by_email(db, new_user.email) is not None :
        raise HTTPException(status_code=400, detail="Email already exist!" )
    
    if crud.get_user_by_username(db, new_user.username) is not None:
        raise HTTPException(status_code=400, detail="Username already exist!")
    
    user = crud.create_user(db,new_user)
    return user
    
@app.post("/users/login", status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,user.email)
    
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    if not auth.verify_password(user.password, db_user.password_hash ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    db_user.last_login=datetime.now(timezone.utc)
    db.commit()
    
    token = auth.create_access_token({"sub": str(db_user.user_id), "role": db_user.user_role})
    return TokenResponse(access_token=token)
           

@app.get("/users/profile", response_model=UserResponse,status_code=200)
def get_my_profile(current_user = Depends(get_current_user)):
    return current_user
    
    
@app.put("/users/update", response_model=UserResponse)
def update_my_profile(data: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.email:
        user_by_email = crud.get_user_by_email(db,data.email)
        if user_by_email and user_by_email.user_id != current_user.user_id:
            raise HTTPException(status_code=400, detail="Email already taken")
    return crud.update_user(db,current_user.user_id,data)
    

@app.delete("/users/delete")
def deactivate_my_account(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.deactivate_user(db, current_user.user_id)
    return {"detail": "Account deactivated successfully"}

@app.get("/users",response_model = List[UserResponse])
def users(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user.user_role == 'admin':
        return crud.get_all_users(db)
    
    raise HTTPException(status_code=403, detail= "Unauthorized User ")