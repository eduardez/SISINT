import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PySide2.QtWidgets import QHeaderView
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons

from Presentacion import ControllerDebug


class Menu:
    def __init__(self, WPController = None):
        super(Menu, self).__init__()
        self.ui = QUiLoader().load(QFile("Presentacion/UI_Files/UI_menu.ui"))
        self.wp_controller = WPController
        self.setActions()
        self.adjustTables()
        self.ui.stackedWidget.setCurrentIndex(3)

    def _exec(self):
        self.ui.show()

    def setActions(self):
        self.ui.btn_enviar.clicked.connect(self.enviarmsg)
        self.ui.btn_mensajes.clicked.connect(self.mensajes)
        self.ui.btn_colegios.clicked.connect(self.colegio)
        self.ui.btn_settings.clicked.connect(self.openDebugSettings)

    def adjustTables(self):
        tablas = [self.ui.tableWidget, self.ui.tbl_alumnos, self.ui.tbl_clases]
        for tbl in tablas:
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

    def openDebugSettings(self):
        deb = ControllerDebug.DebugFrame(self.wp_controller)
        deb.ui.exec_()
        
