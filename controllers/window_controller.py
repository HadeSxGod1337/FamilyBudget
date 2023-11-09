from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QHeaderView

from models.user import User
from models.category import CategoryTransaction
from models.type import TypeTransaction
from models.transaction import Transaction, TransactionsModel
from models.info_model import InfoModel
from controllers.db_controller import DataBaseController

from views.view import MainWindow, RegistrationWindow, LoginWindow, show_message, show_yes_no, ChangeUserWindow


class WindowController:
    def __init__(self, db_controller):
        super().__init__()
        self.main: MainWindow = MainWindow()
        self.reg: RegistrationWindow = RegistrationWindow()
        self.login: LoginWindow = LoginWindow()
        self.change: ChangeUserWindow = ChangeUserWindow()
        self.info: InfoModel = InfoModel(account=0, login=None, name=None, surname=None)
        self.db_controller: DataBaseController = db_controller
        self.transactions_model = TransactionsModel(self.db_controller.get_transactions())
        self.main.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.main.tableView.setModel(self.transactions_model)

        self.change.accept_user.clicked.connect(lambda: self.update_user(*self.change.get_info()))
        self.main.changeUser.clicked.connect(self.open_update)
        self.login.sign_up.clicked.connect(self.login_to_registration)
        self.reg.sign_up.clicked.connect(self.sign_up)
        self.login.login_button.clicked.connect(self.log_in)
        self.main.types.activated.connect(self.add_type)
        self.main.categories.activated.connect(self.add_category)
        self.main.amount.setValidator(QDoubleValidator(0, 100, 100, self.main.amount))
        self.main.createTransaction.clicked.connect(self.add_transaction)
        self.main.deleteCategory.clicked.connect(lambda: show_yes_no("Удаление категории",
                                                                     "Вы точно хотите удалить категорию?",
                                                                     "Вы также удалите все транзакции с этой "
                                                                     "категорией!",
                                                                     self.delete_category)
        if self.main.categories.currentText() else None)
        self.main.deleteType.clicked.connect(lambda: show_yes_no("Удаление типа",
                                                                 "Вы точно хотите удалить тип?",
                                                                 "Вы также удалите все транзакции с этим типом!",
                                                                 self.delete_type)
        if self.main.types.currentText() else None)
        self.change.delete_user.clicked.connect(lambda: show_yes_no("Удаление пользователя",
                                                                 "Вы точно хотите удалить данного пользователя?",
                                                                 "Вы также удалите все транзакции с этим типом!",
                                                                 self.delete_user))


        self.main.categories.addItems(CategoryTransaction.list_name(self.db_controller.session))
        self.main.types.addItems(TypeTransaction.list_name(self.db_controller.session))
        self.main.choose_categoty.addItems(["Все категории"] + list(CategoryTransaction.list_name(self.db_controller.session)))
        self.main.choose_type.addItems(["Все типы"] + list(TypeTransaction.list_name(self.db_controller.session)))
        self.main.choose_user.addItems(["Все пользователи"] + list(User.login_name(self.db_controller.session)))
        self.main.choose_categoty.activated.connect(self.update_table)
        self.main.choose_type.activated.connect(self.update_table)
        self.main.choose_user.activated.connect(self.update_table)
        self.login.show()

    def add_type(self):
        type_name = self.main.types.currentText()
        if self.db_controller.add_type(type_name):
            self.main.choose_type.addItem(type_name)
            show_message("Добавление типа", f"Тип {type_name} успешно добавлен")

    def add_category(self):
        category_name = self.main.categories.currentText()
        if self.db_controller.add_category(category_name):
            self.main.choose_categoty.addItem(category_name)
            show_message("Добавление категории", f"Категория {category_name} успешно добавлена")

    def add_transaction(self):
        category_name = self.main.categories.currentText()
        type_name = self.main.types.currentText()
        if self.main.amount.text() != "":
            amount = float(".".join(self.main.amount.text().split(",")))
        else:
            show_message("Добавление транзакции", "Величина транзакции не может быть пустой")
            return
        login = self.info.login
        if self.db_controller.add_transaction(login, type_name, category_name, amount):
            show_message("Добавление транзакции", "Транзакция успешно добавлена")
            self.update_table()
        else:
            show_message("Добавление транзакции", "Такая транзакция уже существует")

    def update_table(self):
        try:
            texts = [self.main.choose_user.currentText(),
                     self.main.choose_type.currentText(),
                     self.main.choose_categoty.currentText()]
            result = self.db_controller.get_choose_transactions(*texts)
            if result is None:
                self.transactions_model.setItems(self.db_controller.get_transactions())
            else:
                self.transactions_model.setItems(result)
        except Exception as e:
            print("update: ", e)

    def update_type(self):
        self.main.types.clear()
        self.main.types.addItems(TypeTransaction.list_name(self.db_controller.session))

    def update_category(self):
        self.main.categories.clear()
        self.main.categories.addItems(CategoryTransaction.list_name(self.db_controller.session))

    def delete_user(self, can_delete):
        if can_delete:
            self.db_controller.delete_user_by_login(self.info.login)
            self.info.login, self.info.name, self.info.surname = None, None, None
            self.main_to_login()

    def delete_type(self, can_delete):
        if can_delete:
            self.db_controller.delete_type_by_type_name(self.main.types.currentText())
            self.update_type()
            self.update_table()

    def delete_category(self, can_delete):
        if can_delete:
            self.db_controller.delete_category_by_category_name(self.main.categories.currentText())
            self.update_category()
            self.update_table()

    def login_to_registration(self):
        self.reg.show()
        self.login.hide()

    def login_to_main(self):
        self.main.show()
        self.login.hide()

    def reg_to_main(self):
        self.main.show()
        self.reg.hide()

    def main_to_login(self):
        self.login.show()
        self.main.hide()
        self.change.hide()

    def open_update(self):
        self.change.set_info(self.info.name, self.info.surname, self.info.login)
        self.change.show()

    def log_in(self):
        user: User = self.db_controller.get_user_by_login(self.login.login.text())
        if user is not None:
            self.login.login.setText("")
            self.change_user(user.name, user.surname, user.login)
            self.login_to_main()
        else:
            show_message("Ошибка", "Такого пользователя не существует или возникла какая-то ошибка")

    def sign_up(self):
        name, surname, login = self.reg.get_info().values()
        if self.db_controller.add_user(name, surname, login):
            show_message("Успешно", "Пользователь успешно добавлен")
            self.change_user(name, surname, login)
            self.reg_to_main()
        else:
            show_message("Ошибка", "Такой пользователь уже существует")

    def change_user(self, name, surname, login):
        self.info.change_user(name, surname, login)
        self.main.fullUserName.setText(self.info.get_full_name())

    def update_user(self, name, surname, login):
        if self.db_controller.change_user(name, surname, login):
            self.change_user(name, surname, login)
            self.update_table()