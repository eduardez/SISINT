import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons


class DebugFrame():
    def __init__(self, wp_instance):
        super(DebugFrame, self).__init__()
        self.ui = QUiLoader().load(QFile("./Presentacion/UI_Files/UI_Pruebas.ui"))
        ###Para windows (SEVILLA)
        #self.ui = QUiLoader().load(QFile("C:\\Users\\sevil\\Desktop\\SISINT-Controlador\\Presentacion\\UI_Files\\UI_Pruebas.ui"))
        self.wp_instance = wp_instance
        self.setActions()

    def setActions(self):
        self.ui.btn_enviar_msg.clicked.connect(self.enviarMensaje)
        self.ui.btn_buscar_contacto.clicked.connect(self.buscarUser)

    def enviarMensaje(self):
        numero = self.ui.input_numero_envio.text()
        mensaje = self.ui.input_mensaje_envio.text()
        isEnvioActivado = self.ui.is_envio_activado.isChecked()
        self.wp_instance.searchAndClick(numero)
        self.wp_instance.sendMsg(mensaje, isEnvioActivado)

    def buscarUser(self):
        numero = self.ui.input_buscar_contacto.text()
        print(numero)
        self.wp_instance.searchUser(numero)
