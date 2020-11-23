import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons
import webbrowser
from threading import Thread

class Login():
    def __init__(self):
        super(Login, self).__init__()
        self.ui = QUiLoader().load(QFile("Presentacion/UI_Files/UI_login.ui"))
        ### PARA WINDOWS (SEVILLA)
        # self.ui = QUiLoader().load(QFile("C:\\Users\\sevil\\Desktop\\SISINT-persistencia\\Presentacion\\UI_Files\\UI_login.ui"))
        self.ui.btn_iniciar.clicked.connect(self.abrir_menu)
        self.isLogged = False
        self.result_login = None

    def abrir_menu(self):
        usuario = self.ui.le_usuario.text()
        password = self.ui.le_password.text()
        if usuario == "admin" and password == "admin":
            self.isLogged = True
            self.ui.accept()
        else:
            self.ui.lbl_ERROR_user.resize(30, 30)
            self.ui.lbl_ERROR_pass.resize(30, 30)
            self.ui.lbl_error_auth.setText('Error al autenticar')
            print(self.ui.le_usuario.text())
        # aqui hay que añadir una serie de elifs o else en el que mostramos un mensaje diciendo que el usuario o
        # contraseña introducidos son incorrectos, borramos los cmapos de le_usuario y y le_password y le pedimos que
        # lo introduzca de nuevo considerar en un futuro tener en la base de datos las cuentas registradas a la hora
        # de hacer el login de forma mas profesional
    
    def _exec(self):
        self.ui.show()