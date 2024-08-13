#!/usr/bin/env python3
""" user.py """
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    """ User Class """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250))
    reset_token = Column(String(250))
