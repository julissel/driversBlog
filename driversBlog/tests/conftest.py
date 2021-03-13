import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


db_engine = create_engine("sqlite://", echo=False)
# echo=True create log with using module logging

Base = declarative_base(bind=db_engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(db_engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=db_engine)
