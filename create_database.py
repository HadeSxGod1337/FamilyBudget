from models.database import create_db, Session
from models.user import User
from models.transaction import Transaction
from models.category import CategoryTransaction
from models.type import TypeTransaction


def create_database(load_example_data: bool = True):
    create_db()
    if load_example_data:
        _load_example_data(Session())


def _load_example_data(session: Session):
    session.add(User(name="Данил", surname="Коршунов", login="k"))
    session.commit()
    session.add(TypeTransaction(type_name="Приход"))
    session.commit()
    session.add(CategoryTransaction(category_name="Зарплата"))
    session.commit()
    session.close()
