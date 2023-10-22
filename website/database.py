from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, DateTime

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


Base = declarative_base()
class Visit(Base):
    __tablename__ = "site_visits"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    img_name = Column(String)
    animal = Column(String)

SessionLocal = sessionmaker(autoflush=False, bind=engine)