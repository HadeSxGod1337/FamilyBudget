from sqlalchemy import Column, Integer, String
from models.database import Base


class TypeTransaction(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String, nullable=False, unique=True)

    def __init__(self, type_name: str):
        self.type_name = type_name

    def __str__(self):
        return self.type_name

    @staticmethod
    def list(session):
        query = session.query(TypeTransaction)
        result = query.all()
        for item in result:
            yield item
        return

    @staticmethod
    def list_name(session):
        query = session.query(TypeTransaction)
        result = query.all()
        for item in result:
            yield item.type_name
        return
