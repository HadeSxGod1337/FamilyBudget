from dataclasses import dataclass


@dataclass
class InfoModel:
    account: int | None
    login: str | None
    name: str | None
    surname: str | None

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def change_user(self, name, surname, login):
        self.name = name
        self.surname = surname
        self.login = login
