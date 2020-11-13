import sys

from PyQt5.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from Resources import login_resources_rc


class Login:
    def __init__(self):
        super(Login, self).__init__()
        self.ui = QUiLoader().load(QFile("UI_login.ui"))
        self.ui.btn_iniciar.clicked.connect(self.open_menu)
        self.menu = Menu()

    def open_menu(self):
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





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Login()
    myapp.ui.show()
    sys.exit(app.exec_())
