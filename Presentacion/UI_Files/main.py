import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from Resources import icons
import webbrowser


class Login:
    def __init__(self):
        super(Login, self).__init__()
        self.ui = QUiLoader().load(QFile("UI_login.ui"))
        self.ui.btn_iniciar.clicked.connect(self.abrir_menu)
        self.menu = Menu()

    def abrir_menu(self):
        usuario = self.ui.le_usuario.text()
        password = self.ui.le_password.text()
        if usuario == "admin" and password == "admin":
            self.menu.ui.show()
        # aqui hay que añadir una serie de elifs o else en el que mostramos un mensaje diciendo que el usuario o
        # contraseña introducidos son incorrectos, borramos los cmapos de le_usuario y y le_password y le pedimos que
        # lo introduzca de nuevo considerar en un futuro tener en la base de datos las cuentas registradas a la hora
        # de hacer el login de forma mas profesional




class Menu:
    def __init__(self):
        super(Menu, self).__init__()
        self.ui = QUiLoader().load(QFile("UI_menu.ui"))
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.btn_enviar.clicked.connect(self.enviarmsg)
        self.ui.btn_mensajes.clicked.connect(self.mensajes)
        self.ui.btn_colegios.clicked.connect(self.colegio)
    def enviarmsg(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btn_forms.clicked.connect(self.crear_googleforms)
    def crear_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/')

    def mensajes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btn_masivo.clicked.connect(self.ver_googleforms)
    def ver_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/')


    def colegio(self):
        self.ui.stackedWidget.setCurrentIndex(2)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Login()
    myapp.ui.show()
    sys.exit(app.exec_())
