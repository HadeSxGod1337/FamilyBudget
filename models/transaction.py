from sqlalchemy import Column, Integer, ForeignKey, Float
from models.database import Base
from sqlalchemy.orm import relationship
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
import operator

from functools import cached_property


class TransactionsModel(QAbstractItemModel):
    def __init__(self, items):
        super(TransactionsModel, self).__init__()
        self._items = items
        self._header_data = {
            0: "id",
            1: "Пользователь",
            2: "Тип транзакции",
            3: "Категория транзакции",
            4: "Величина"
        }

    def parent(self, index):
        parent_item = index.internalPointer()
        if not parent_item:
            return QModelIndex()
        row = self._items.index(parent_item)
        return self.createIndex(row, 0, None)

    def index(self, row, col, parent=QModelIndex()):
        if (row < 0 or row >= self.rowCount(parent) or
                col < 0 or col >= self.columnCount(parent)):
            return QModelIndex()
        if parent.isValid():
            if parent.column() != 0:
                return QModelIndex()
            # store a pointer to the parent category in internalPointer
            return self.createIndex(row, col, self._items[parent.row()])
        return self.createIndex(row, col, None)

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self.setItems(sorted(self._items, key=operator.itemgetter(column)))
        if order == Qt.DescendingOrder:
            self._items.reverse()
        self.layoutChanged.emit()

    def setItems(self, items):
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:

        return len(self._items)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 5

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = ...):
        if role == Qt.DisplayRole:
            try:
                return self._items[index.row()][index.column()]
            except IndexError:
                return "IndexError"
        elif role == Qt.UserRole:
            return self._items[index.row()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header_data.get(section)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type_transaction_id = Column(
        Integer,
        ForeignKey('types.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    category_transaction_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    amount = Column(Float)

    user = relationship("User", backref="transactions", foreign_keys=[user_id])
    type = relationship("TypeTransaction", backref="transactions", foreign_keys=[type_transaction_id])
    category = relationship("CategoryTransaction", backref="transactions", foreign_keys=[category_transaction_id])

    def __init__(self, user, type, category, amount):
        self.user = user
        self.type = type
        self.category = category
        self.amount = amount

    def __repr__(self):
        return (
                f'<Transaction(user="{self.user.surname} {self.user.name}" type={self.type} '
                + f'category={self.category} amount="{self.amount}")>'
        )

    @staticmethod
    def list(session):
        query = session.query(Transaction)
        result = query.all()
        transactions = []
        for item in result:
            transactions.append([str(item.id), f"{item.user.surname} {item.user.name}", item.type.type_name,
                                 item.category.category_name, str(item.amount)])
        return transactions

    @staticmethod
    def list_item(session):
        query = session.query(Transaction)
        result = query.all()
        for item in result:
            yield item
        return
