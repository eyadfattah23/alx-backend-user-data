#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save a user to the database.

        Args:
            email (str)
            hashed_password (str)
        """
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()

        return usr

    def find_user_by(self, **kwargs) -> User:
        """return the first row found in the users table
            filtered by the input arguments.
        """
        user_keys = list(User.__dict__.keys())
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError

        filtered_user = self._session.query(User).filter_by(**kwargs).first()

        if not filtered_user:
            raise NoResultFound
        return filtered_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update a user having user_id, using the provided kwargs

        Args:
            user_id (int): user id
        """
        user_keys = list(User.__dict__.keys())
        for key in kwargs.keys():
            if key not in user_keys:
                raise ValueError
        try:
            usr = self.find_user_by(id=user_id)
        except (InvalidRequestError, NoResultFound) as IRE:
            raise ValueError
        if not usr:
            raise ValueError

        usr.__dict__.update(**kwargs)

        return None
