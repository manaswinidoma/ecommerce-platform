from models import User
from schemas import UserRegister
from auth import hash_password

def get_user_by_email(db,email):
    return db.query(User).filter(User.email==email).first()   
    
def get_user_by_id(db, user_id):
    return db.query(User).filter(User.user_id==user_id).first()

def get_user_by_username(db, username):
    return db.query(User).filter(User.username==username).first()

def create_user(db, user: UserRegister):
    hashed = hash_password(user.password)
    db_user = User(
        username = user.username,
        firstname= user.firstname,
        lastname= user.lastname,
        email=user.email,
        password_hash=hashed,
        date_of_birth=user.date_of_birth
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
    
    
def update_user(db, user_id, data):
    user = db.query(User).filter(User.user_id==user_id).first()
    
    if user:
        update_data = data.dict(exclude_unset=True) #this tells Pydantic to only include fields the user actually sent, ignoring fields they didn't include in the request
        for key, value in update_data.items():
            setattr(user, key, value)    
            
        db.commit()
        db.refresh(user)
    return user

def deactivate_user(db, user_id):
    user = db.query(User).filter(User.user_id==user_id).first()    
    
    if user:
        user.is_active = False
        db.commit()
        db.refresh(user)
        
    return user
        
    