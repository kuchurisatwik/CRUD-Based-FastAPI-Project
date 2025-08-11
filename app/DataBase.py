from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# echo=True will log all SQLAlchemy activity—handy for debugging
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Use a capitalized name for the session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Declarative base class for our ORM models
Base = declarative_base()
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user = 'postgres',
#                                 password = 'Satwik@777',cursor_factory = RealDictCursor)
#         cursor  = conn.cursor()
#         print("db conn was successful")
#         break

#     except Exception as error:
#         print("connecting to db failed")
#         print("error: ", error)
#         time.sleep(2)





