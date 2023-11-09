from models.user import User
from models.category import CategoryTransaction
from models.type import TypeTransaction
from models.transaction import Transaction
from sqlalchemy import exists, delete, update
from sqlalchemy.dialects import sqlite
from sqlalchemy.sql import and_


class DataBaseController:
    def __init__(self, session):
        self.__session = session

    @property
    def session(self):
        return self.__session

    @staticmethod
    def change_database(func):

        def _wrapper(*args, **kwargs):
            session = args[0].session
            try:
                result = func(*args)
                session.commit()
                session.close()
                return result
            except Exception as e:
                session.rollback()
                print("Ошибка: ", e)
                return False

        return _wrapper

    """get_info_from_db"""

    def get_transactions(self):
        return Transaction.list(self.session)

    def get_choose_transactions(self, login=None, type_name=None, category_name=None):
        try:
            user = self.get_user_by_login(login) \
                if login in User.login_name(self.session) else None
            category = self.get_category(category_name) \
                if category_name in CategoryTransaction.list_name(self.session) else None
            type = self.get_type(type_name) \
                if type_name in TypeTransaction.list_name(self.session) else None
            transactions = self.session.query(Transaction)
            if user is not None:

                transactions = transactions.filter(Transaction.user_id == user.id)
            if type is not None:
                transactions = transactions.filter(Transaction.type_transaction_id == type.id)
            if category is not None:
                transactions = transactions.filter(Transaction.category_transaction_id == category.id)

            transactions = transactions.all()
            return Transaction.get_info_from_transaction_model(transactions)
        except Exception as e:
            print("error:", e)

    def get_category(self, category_name):
        category = self.session.query(CategoryTransaction).filter(
            CategoryTransaction.category_name == category_name).first()
        return category

    def get_type(self, type_name):
        return self.session.query(TypeTransaction).filter(TypeTransaction.type_name == type_name).first()

    def get_user_by_login(self, login):
        return self.session.query(User).filter(User.login == login).first()

    @change_database
    def change_user(self, name, surname, login):
        user = self.get_user_by_login(login)
        if user.name != name or user.surname != surname:
            query = update(User).where(User.id == user.id).values(name=name, surname=surname, login=login)
            query.compile(dialect=sqlite.dialect())
            self.session.execute(query)
            return True
        return True

    """add_info_to_db"""

    @change_database
    def add_user(self, name, surname, login):
        if not self.session.query(exists().where(User.login == login)).scalar():
            new_user = User(name=name, surname=surname, login=login)
            self.session.add(new_user)
            return True
        return False

    @change_database
    def add_type(self, type_name):
        if not self.session.query(exists().where(TypeTransaction.type_name == type_name)).scalar():
            new_type = TypeTransaction(type_name)
            self.session.add(new_type)
            return True
        return False

    @change_database
    def add_category(self, category_name):
        if not self.session.query(exists().where(CategoryTransaction.category_name == category_name)).scalar():
            new_category = CategoryTransaction(category_name)
            self.session.add(new_category)
            return True
        return False

    @change_database
    def add_transaction(self, login, type_name, category_name, amount):
        user = self.get_user_by_login(login)
        type = self.get_type(type_name)
        category = self.get_category(category_name)
        new_transaction = Transaction(user, type, category, amount)
        self.session.add(new_transaction)
        return True

    """delete_info_from_db"""

    @change_database
    def delete_user_by_login(self, login):
        user = self.get_user_by_login(login)
        self.session.delete(user)

    @change_database
    def delete_category_by_category_name(self, category_name):
        category = self.get_category(category_name)
        query = delete(Transaction).where(Transaction.category_transaction_id == category.id)
        query.compile(dialect=sqlite.dialect())
        self.session.execute(query)
        self.delete_category(category)

    @change_database
    def delete_category(self, category):
        self.session.delete(category)

    @change_database
    def delete_type_by_type_name(self, type_name):
        type = self.get_type(type_name)
        query = delete(Transaction).where(Transaction.type_transaction_id == type.id)
        query.compile(dialect=sqlite.dialect())
        self.session.execute(query)
        self.delete_type(type)

    @change_database
    def delete_type(self, type):
        self.session.delete(type)