from sqlalchemy import Column, Integer, String
from models.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)

    def __init__(self, name: str, surname: str, login: str):
        self.name = name
        self.surname = surname
        self.login = login

    def __repr__(self):
        return f'<User(name="{self.name}", surname="{self.surname}, login="{self.login}")>'

    @staticmethod
    def list_name(session):
        query = session.query(User)
        result = query.all()
        for item in result:
            yield item.name
        return

    @staticmethod
    def login_name(session):
        query = session.query(User)
        result = query.all()
        for item in result:
            yield item.login
        return
