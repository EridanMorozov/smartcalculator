import sqlite3
import sys

from PyQt5 import uic, QtWidgets, sip
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)
        self.setFixedSize(487, 694)  # фикс. размер
        # кнопки калькулятора
        self.oper = str('')
        self.tot = str('')
        self.itog = []
        self.result = ''
        self.btn1.clicked.connect(self.btn_1)
        self.btn2.clicked.connect(self.btn_2)
        self.btn3.clicked.connect(self.btn_3)
        self.btn4.clicked.connect(self.btn_4)
        self.btn5.clicked.connect(self.btn_5)
        self.btn6.clicked.connect(self.btn_6)
        self.btn7.clicked.connect(self.btn_7)
        self.btn8.clicked.connect(self.btn_8)
        self.btn9.clicked.connect(self.btn_9)
        self.btn0.clicked.connect(self.btn_0)
        self.btn_eq.clicked.connect(self.eq)
        self.btn_plus.clicked.connect(self.plus)
        self.btn_minus.clicked.connect(self.minus)
        self.btn_mult.clicked.connect(self.mult)
        self.btn_div.clicked.connect(self.div)
        self.btn_clear.clicked.connect(self.reset)
        self.btn_dot.clicked.connect(self.bot)
        self.btn_fact.clicked.connect(self.fac)
        self.btn_pow.clicked.connect(self.pow)
        self.btn_sqrt.clicked.connect(self.bn_sqrt)
        self.btn_formulas.clicked.connect(self.form)

    # функции кнопок
    def btn_1(self):
        self.oper += '1'
        self.tot += '1'
        self.table.display(self.oper)

    def btn_2(self):
        self.oper += '2'
        self.tot += '2'
        self.table.display(self.oper)

    def btn_3(self):
        self.oper += '3'
        self.tot += '3'
        self.table.display(self.oper)

    def btn_4(self):
        self.oper += '4'
        self.tot += '4'
        self.table.display(self.oper)

    def btn_5(self):
        self.oper += '5'
        self.tot += '5'
        self.table.display(self.oper)

    def btn_6(self):
        self.oper += '6'
        self.tot += '6'
        self.table.display(self.oper)

    def btn_7(self):
        self.oper += '7'
        self.tot += '7'
        self.table.display(self.oper)

    def btn_8(self):
        self.oper += '8'
        self.tot += '8'
        self.table.display(self.oper)

    def btn_9(self):
        self.oper += '9'
        self.tot += '9'
        self.table.display(self.oper)

    def btn_0(self):
        self.oper += '0'
        self.tot += '0'
        self.table.display(self.oper)

    def plus(self):
        self.tot += ' + '
        self.oper = ''
        self.table.display(self.oper)

    def minus(self):
        self.tot += ' - '
        self.oper = ''
        self.table.display(self.oper)

    def mult(self):
        self.tot += ' * '
        self.oper = ''
        self.table.display(self.oper)

    def div(self):
        self.tot += ' / '
        self.oper = ''
        self.table.display(self.oper)

    def bot(self):
        self.tot += '.'
        self.oper += '.'
        self.table.display(self.oper)

    def fac(self):
        n = 1
        for i in range(1, int(self.tot) + 1):
            n *= i
        self.tot = ''
        self.oper = str(n)
        self.tot += str(n)
        self.result = self.tot
        self.table.display(self.oper)

    def pow(self):
        self.tot += ' ** '
        self.oper = ''
        self.table.display(self.oper)

    def bn_sqrt(self):
        self.oper = ''
        a = int(self.tot) ** 0.5
        self.tot = ''
        self.oper += str(a)
        self.tot += str(a)
        self.result = self.tot
        self.table.display(self.oper)

    def reset(self):
        self.tot = ''
        self.oper = ''
        self.result = 0
        self.table.display(self.result)

    def eq(self):
        itog = self.tot.split(' / ')
        if ' / ' in self.tot and itog[-1] == '0':  # проверка деления на ноль
            self.table.display('Error')
        else:
            self.result = eval(self.tot)
            self.table.display(self.result)
            self.tot = str(self.result)

    def form(self):
        self.btn_formulas.clicked.connect(self.open_second_page)  # привязка функции к кнопке

    def open_second_page(self):  # функция открытия второго окна
        self.second_window = SecondWindow(self)
        self.second_window.show()


class SecondWindow(QMainWindow):  # класс второго окна
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('subject.ui', self)
        self.setFixedSize(992, 678)  # фикс. размер
        self.dictionary = {}
        self.con = sqlite3.connect('db.sqlite')
        self.cur = self.con.cursor()

        self.request_to_formulas()
        self.btn_search.clicked.connect(self.search)

    def search(self):
        self.btn_search.clicked.connect(self.searchforsubject)

    def request_to_formulas(self):
        req = self.cur.execute('''SELECT * 
                                FROM subjects''').fetchall()  # выбор таблицы из которой будут браться данные

        for value, key in req:
            self.dictionary[key] = value

        for i in self.dictionary.keys():
            self.comboBox.addItem(i)

    def searchforsubject(self):
        name = self.comboBox.currentText()
        title = self.dictionary.get(name)
        req = self.cur.execute(f'''
                    SELECT class, theme, formula 
                        FROM formulas 
                            WHERE subject = {title}''').fetchall()
        for i, elem in enumerate(req):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
