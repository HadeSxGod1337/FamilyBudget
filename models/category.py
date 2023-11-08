from sqlalchemy import Column, Integer, String
from models.database import Base
from sqlalchemy.orm import relationship


class CategoryTransaction(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False, unique=True)

    def __init__(self, category_name: str):
        self.category_name = category_name

    def __str__(self):
        return self.category_name

    @staticmethod
    def list(session):
        query = session.query(CategoryTransaction)
        result = query.all()
        for item in result:
            yield item
        return

    @staticmethod
    def list_name(session):
        query = session.query(CategoryTransaction)
        result = query.all()
        for item in result:
            yield item.category_name
        return
