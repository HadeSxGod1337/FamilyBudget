import os

from models.database import DATABASE_NAME
import create_database as db_creator
from models.database import Session
from PyQt5.QtWidgets import QApplication
from controllers.window_controller import WindowController
from controllers.db_controller import DataBaseController
import sys


class App(QApplication):
    def __init__(self, args, session):
        super().__init__(args)
        self.database_controller = DataBaseController(session)
        self.window_controller = WindowController(self.database_controller)


if __name__ == "__main__":
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        db_creator.create_database()
        print("БД создалась")
    else:
        print("БД уже создана")
    app = App(sys.argv, session=Session())
    app.exec_()
