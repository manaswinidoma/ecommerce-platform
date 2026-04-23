# To manage the database connection
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv() 
database_url = os.getenv("DATABASE_URL") 

Base = declarative_base()

engine = create_engine( database_url, 
                        pool_size = 5,  #core infra, acts as gateway to database
                        max_overflow = 10,
                        pool_timeout = 30,
                        pool_recycle = 3600)

SessionLocal = sessionmaker(       #session factory responsible for spawning the session objects
                autocommit=False,  # transactions are controlled manually
                autoflush=False,   # changes are not automatically pushed to db before queries
                bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()