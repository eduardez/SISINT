# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from Presentacion.UI_Files.UI_Principal import Ui_MainWindow

import sys 

class Ui_Principal(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, frame, wp_instance, parent = None):
        super(Ui_Principal, self).__init__(parent)

        # --- Init methods ---
        self.wp_instance = wp_instance
        self.frm_principal = frame
        self.setupUi(self.frm_principal)
        self.setActions()

    def setActions(self):
        self.btn_enviar_msg.clicked.connect(lambda: self.enviarMensaje())
        self.actionAbrir_guasa.triggered.connect(lambda: self.abrirPagina())

    def abrirPagina(self):
        self.wp_instance.startConnection()

    def enviarMensaje(self):
        pass



def limpiarRecursos(wp_instance):
    '''Cierra la instancia de Chrome y otras cosas'''
    wp_instance.closeDriver()
    print('Cerrao')


def start(wp_instance):
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: limpiarRecursos(wp_instance))
    #app.setStyle('Fusion')
    frm_principal = QtWidgets.QMainWindow()
    ui = Ui_Principal(frm_principal, wp_instance)
    ui.frm_principal.show()
    sys.exit(app.exec_())