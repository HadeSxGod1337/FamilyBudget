from views.login import Ui_Login
from views.registration import Ui_Registration
from views.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt


def show_message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Cancel)
    msg.exec()


def show_yes_no(title, text, inf_text, func_yes):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setInformativeText("<span style='color: red'>" + inf_text + "</span>")

    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.buttonClicked.connect(lambda btn: func_yes(msg.standardButton(msg.clickedButton()) == QMessageBox.Yes))
    msg.exec()


class ChangeUserWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Изменение пользователя")
        self.setMinimumSize(400, 200)
        self.login = QLineEdit(self)
        self.name = QLineEdit(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.surname = QLineEdit(self)
        self.label_login = QLabel(self)
        self.label_login.setText("Ваш логин")
        self.label_name = QLabel(self)
        self.label_name.setText("Измените Ваше имя")
        self.label_surname = QLabel(self)
        self.label_surname.setText("Измените Вашу фамилию")
        self.accept_user = QPushButton(self)
        self.accept_user.setText("Подтвердить изменения")
        self.delete_user = QPushButton(self)
        self.delete_user.setText("Удалить пользователя")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label_login)
        layout.addWidget(self.login)
        layout.addWidget(self.label_name)
        layout.addWidget(self.name)
        layout.addWidget(self.label_surname)
        layout.addWidget(self.surname)
        layout.addWidget(self.accept_user)
        layout.addWidget(self.delete_user)

        self.login.setEnabled(False)

    def show(self):
        self.showMaximized()
        qtRectangle = self.frameGeometry()
        CenterPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(CenterPoint)
        self.move(qtRectangle.topLeft())

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        self.resize(width, height)

    def set_info(self, name, surname, login):
        self.name.setText(name)
        self.surname.setText(surname)
        self.login.setText(login)

    def get_info(self):
        self.hide()
        return self.name.text(), self.surname.text(), self.login.text()


class RegistrationWindow(QMainWindow, Ui_Registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def get_info(self):
        return {"name": self.input_name.text(),
                "surname": self.input_surname.text(),
                "login": self.login.text()}


class LoginWindow(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.policies = [
            'Не изменять',
            'Добавить',
            'InsertAtCurrent',
            'InsertAtBottom',
            'InsertAfterCurrent',
            'InsertBeforeCurrent',
            'InsertAlphabetically'
        ]
        self.insertPolicyType.addItems(self.policies)
        self.insertPolicyCategory.addItems(self.policies)
        self.categories.setInsertPolicy(0)
        self.types.setInsertPolicy(0)
        self.insertPolicyCategory.currentIndexChanged.connect(self.categories.setInsertPolicy)
        self.insertPolicyType.currentIndexChanged.connect(self.types.setInsertPolicy)


if __name__ == '__main__':
    pass
