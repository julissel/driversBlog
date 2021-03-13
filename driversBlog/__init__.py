from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


db_engine = create_engine("sqlite:///driversBlog.db", echo=False)
# echo=True create log with using module logging

Base = declarative_base(bind=db_engine)
session = Session()
