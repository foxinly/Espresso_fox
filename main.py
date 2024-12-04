import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.btn.clicked.connect(self.addEditCoffeeForm_function)
        self.close_btn.clicked.connect(self.close_coffee)

    def addEditCoffeeForm_function(self):
        self.create_show = addEditCoffeeForm()
        self.create_show.show()
        self.close()

    def close_coffee(self):
        self.close()


class addEditCoffeeForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        for i in ('Светлая', 'Средняя', 'Темная'):
            self.stepen.addItem(f'{i}')
        for i in ('Молотый', 'В зернах'):
            self.razn.addItem(f'{i}')
        self.create_btn.clicked.connect(self.create_coffee)
        self.change_btn.clicked.connect(self.change_coffee)
        self.close_btn.clicked.connect(self.close_coffee)
        self.table_coffee.itemChanged.connect(self.item_changed)
        self.kilo.setRange(1, 1000000)
        self.cost.setRange(10,1000000)
        self.modified = {}
        self.titles = list()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        if not result:
            QMessageBox.warning(self, "Ошибка", "Ничего не нашлось в таблице birthday",
                                QMessageBox.StandardButton.Ok)
        else:
            self.table_coffee.setRowCount(len(result))
            self.table_coffee.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.table_coffee.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}

    def create_coffee(self):
        name_ok = self.check_name(self.name.text())
        if name_ok:
            cur.execute(f"""INSERT INTO coffee(Сорт, Обжарка, Разновидность, Описание, Цена,  Объем)
                            VALUES ('{self.name.text()}', '{self.stepen.currentText()}', '{self.razn.currentText()}', '{self.text.text()}', {int(self.cost.text())},  {int(self.kilo.text())})""")
            con.commit()
            res = QMessageBox.information(self, "Оповещение", "Вы добавили новый сорт кофе!",
                                          QMessageBox.StandardButton.Ok)
            self.update_wind()

    def check_name(self, name):  # проверка имени:
        try:
            if len(name) > 50:
                raise WrongNameFormat
            if name.strip() != '':  # на пусткую строку
                return True
            else:
                raise EmptyLE
        except EmptyLE:
            QMessageBox.warning(self, 'Ошибка', 'Не заполнено обязтельное поле: name', QMessageBox.StandardButton.Ok)
            return False
        except WrongNameFormat:
            QMessageBox.warning(self, 'Ошибка', 'Неверный формат: name', QMessageBox.StandardButton.Ok)
            return False

    def change_coffee(self):
        try:
            rows = list(set([i.row() for i in self.table_coffee.selectedItems()]))
            ids = [self.table_coffee.item(i, 0).text() for i in rows]
            if self.modified:
                if 'ID' in self.modified.keys():
                    raise NotChangeID
                if ('Цена' in self.modified.keys() or 'Объем' in self.modified.keys()):
                    try:
                        if self.modified['Цена'] < 0:
                            raise MyTypeError
                    except Exception:
                        if self.modified['Объем'] < 0:
                            raise MyTypeError
                que = "UPDATE coffee SET "
                que += ", ".join(
                    [f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
                if que != "UPDATE coffee SET Описание=''" and que != "UPDATE coffee SET Обжарка=''" and \
                        que != "UPDATE coffee SET ID=''" and que != "UPDATE coffee SET Сорт=''" and \
                        que != "UPDATE coffee SET Разновидность=''" and que != "UPDATE coffee SET Цена=''" and \
                        que != "UPDATE coffee SET Объем=''":
                    if "UPDATE coffee SET Разновидность=" in que and (
                            "UPDATE coffee SET Разновидность='Молотый'" != que and "UPDATE coffee SET Разновидность='В зернах'" != que):
                        raise MyTypeError
                    if "UPDATE coffee SET Обжарка=" in que and (
                            "UPDATE coffee SET Обжарка='Светлая'" != que and "UPDATE coffee SET Обжарка='Средняя'" != que \
                            and "UPDATE coffee SET Обжарка='Темная'" != que):
                        raise MyTypeError
                    que += f" WHERE id = '{int(ids[0])}'"
                    print(que)
                    cur.execute(que)
                    con.commit()
                else:
                    raise NullError
                self.modified.clear()
        except NullError:
            QMessageBox.warning(self, "Ошибка", "Значение не может быть равно 0",
                                QMessageBox.StandardButton.Ok)

        except NotChangeID:
            QMessageBox.warning(self, "Ошибка", "Значение не может быть изменено",
                                QMessageBox.StandardButton.Ok)

        except MyTypeError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат ввода данных.",
                                QMessageBox.StandardButton.Ok)

    def update_wind(self):
        self.open_back = addEditCoffeeForm()
        self.open_back.show()
        self.close()


    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def close_coffee(self):
        self.open_main = Coffee()
        self.open_main.show()
        self.close()


class WrongNameFormat(Exception):
    pass


class EmptyLE(Exception):
    pass


class NullError(Exception):
    pass


class NotChangeID(Exception):
    pass


class MyTypeError(Exception):
    pass


if __name__ == '__main__':
    con = sqlite3.connect('coffee.sqlite')
    cur = con.cursor()
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
