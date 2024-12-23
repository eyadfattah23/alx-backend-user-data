#!/usr/bin/env python3
"""
Create a SQLAlchemy model named User for a database table named users
using the mapping declaration of SQLAlchemy
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, Column, String

Base = declarative_base()


class User(Base):
    """User class

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
